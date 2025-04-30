import sqlite3
import heapq
from collections import defaultdict
from functools import lru_cache
from typing import List, Dict, Optional

GRAPH = defaultdict(dict)
CITY_CACHE = {}


def initialize(db_path: str):
    global GRAPH, CITY_CACHE
    GRAPH = _load_graph(db_path)
    CITY_CACHE = _load_city_cache(db_path)


def _load_graph(db_path: str) -> defaultdict:
    graph = defaultdict(dict)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
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

    for row in cursor:
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

    conn.close()
    return graph


def _load_city_cache(db_path: str) -> dict:
    city_cache = {}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM cities")

    for row in cursor:
        city_cache[row['name']] = row['id']

    conn.close()
    return city_cache


def reload_graph(db_path: str):
    global GRAPH, CITY_CACHE
    GRAPH = _load_graph(db_path)
    CITY_CACHE = _load_city_cache(db_path)
    find_routes.cache_clear()


@lru_cache(maxsize=1000)
def find_routes(
        start_city: str,
        end_city: str,
        criterion: str,
        top_n: int = 5,
        max_cost: Optional[float] = None,
        min_comfort: Optional[float] = None,
        max_transfers: Optional[int] = None
) -> list:

    if not GRAPH:
        raise RuntimeError('load graph first')

    start_id = CITY_CACHE.get(start_city)
    end_id = CITY_CACHE.get(end_city)

    if not start_id or not end_id:
        return []

    if criterion == 'comfort' and max_transfers is None:
        max_transfers = 7

    heap = []
    heapq.heappush(heap, (0, [start_id], [], 0, 0, 0))
    found_routes = []

    while heap and len(found_routes) < top_n:
        current_score, path, segments, current_cost, current_comfort, transfers = heapq.heappop(heap)
        last_node = path[-1]

        if last_node == end_id:
            avg_comfort = current_comfort / len(segments) if segments else 0
            found_routes.append({
                'path': [s['from_city'] for s in segments] + [segments[-1]['to_city']],
                'transport': [s['transport'] for s in segments],
                'segments': segments,
                'total_cost': current_cost,
                'total_time': sum(s['time'] for s in segments),
                'avg_comfort': avg_comfort,
                'transfers': len(segments) - 1
            })
            continue

        for neighbor, data in GRAPH[last_node].items():
            if neighbor not in path:
                new_cost = current_cost + data['cost']
                new_comfort = current_comfort + data['comfort']
                new_transfers = transfers + 1 if segments else 0

                if max_cost is not None and new_cost > max_cost:
                    continue
                if min_comfort is not None and (new_comfort / (len(segments) + 1)) < min_comfort:
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