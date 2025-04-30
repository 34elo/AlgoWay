
import heapq
import asyncio
from collections import defaultdict
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import aiosqlite

GRAPH = defaultdict(dict)
CITY_CACHE = {}
GRAPH_LOCK = asyncio.Lock()
CACHE_LOCK = asyncio.Lock()


async def initialize(db_path: str):
    async with GRAPH_LOCK, CACHE_LOCK:
        global GRAPH, CITY_CACHE
        GRAPH = await _load_graph_async(db_path)
        CITY_CACHE = await _load_city_cache_async(db_path)


async def _load_graph_async(db_path: str) -> defaultdict:
    graph = defaultdict(dict)

    async with aiosqlite.connect(db_path) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.cursor()

        await cursor.execute("""
                             SELECT r.from_city_id,
                                    r.to_city_id,
                                    r.cost,
                                    r.time_min,
                                    r.comfort,
                                    c1.name as from_city,
                                    c2.name as to_city,
                                    r.transport_type
                             FROM routes r
                                      JOIN cities c1 ON r.from_city_id = c1.id
                                      JOIN cities c2 ON r.to_city_id = c2.id
                             """)

        async for row in cursor:
            from_id = row['from_city_id']
            to_id = row['to_city_id']
            graph[from_id][to_id] = {
                'cost': row['cost'],
                'time': row['time_min'],
                'comfort': row['comfort'],
                'from_city': row['from_city'],
                'to_city': row['to_city'],
                'transport': row['transport_type']
            }

    return graph


async def _load_city_cache_async(db_path: str) -> dict:
    city_cache = {}

    async with aiosqlite.connect(db_path) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.cursor()

        await cursor.execute("SELECT id, name FROM cities")

        async for row in cursor:
            city_cache[row['name']] = row['id']

    return city_cache


async def reload_graph_async(db_path: str):
    async with GRAPH_LOCK, CACHE_LOCK:
        global GRAPH, CITY_CACHE
        GRAPH = await _load_graph_async(db_path)
        CITY_CACHE = await _load_city_cache_async(db_path)
        find_routes_async.cache_clear()


def _sync_find_routes(start_city: str, end_city: str, criterion: str,
                      top_n: int, max_cost: Optional[float],
                      min_comfort: Optional[float], max_transfers: Optional[int]) -> List[Dict]:
    if not GRAPH:
        raise RuntimeError('Graph not loaded')

    start_id = CITY_CACHE.get(start_city)
    end_id = CITY_CACHE.get(end_city)

    if not start_id or not end_id:
        return []

    if criterion == 'comfort' and max_transfers is None:
        max_transfers = 7

    heap = []
    heapq.heappush(heap, (0, [start_id], [], 0, 0, 0))  # (score, path, segments, total_cost, total_comfort, transfers)
    found_routes = []

    while heap and len(found_routes) < top_n:
        current_score, path, segments, total_cost, total_comfort, transfers = heapq.heappop(heap)
        last_node = path[-1]

        if last_node == end_id:
            # Проверяем финальные условия по max_cost и min_comfort
            if max_cost is not None and total_cost > max_cost:
                continue
            if min_comfort is not None and (total_comfort / len(segments)) < min_comfort:
                continue

            avg_comfort = total_comfort / len(segments) if segments else 0
            found_routes.append({
                'path': [s['from_city'] for s in segments] + [segments[-1]['to_city']],
                'transport': [s['transport'] for s in segments],
                'segments': segments,
                'total_cost': total_cost,
                'total_time': sum(s['time'] for s in segments),
                'avg_comfort': avg_comfort,
                'transfers': len(segments) - 1
            })
            continue

        for neighbor, data in GRAPH[last_node].items():
            if neighbor in path:
                continue

            new_cost = total_cost + data['cost']
            new_comfort = total_comfort + data['comfort']
            new_transfers = transfers + 1 if segments else 0

            # Ранний выход если маршрут уже превышает max_cost
            if max_cost is not None and new_cost > max_cost:
                continue

            if max_transfers is not None and new_transfers > max_transfers:
                continue

            if criterion == 'cost':
                new_score = new_cost
            elif criterion == 'time_min':
                new_score = current_score + data['time']
            else:  # comfort
                comfort_penalty = new_transfers * 5
                new_score = current_score - (data['comfort'] - comfort_penalty)

            heapq.heappush(
                heap,
                (
                    new_score,
                    path + [neighbor],
                    segments + [data],
                    new_cost,
                    new_comfort,
                    new_transfers
                )
            )

    if criterion == 'comfort':
        found_routes.sort(key=lambda x: -x['avg_comfort'])

    return found_routes[:top_n]

async def find_routes_async(
    start_city: str,
    end_city: str,
    criterion: str,
    top_n: int = 5,
    max_cost: Optional[float] = None,
    min_comfort: Optional[float] = None,
    max_transfers: Optional[int] = None
) -> List[Dict]:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(
            pool,
            _sync_find_routes,
            start_city, end_city, criterion, top_n,
            max_cost, min_comfort, max_transfers
        )