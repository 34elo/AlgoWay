import sqlite3
import heapq
from collections import defaultdict

if __name__ == '__main__':
    path_db = '../data/database.db'
else:
    path_db = './app/data/database.db'


def find_cheapest_routes(start_city: str, end_city: str, top_n: int = 5) -> list:
    return find_optimal_routes(start_city, end_city, 'cost', top_n)


def find_fastest_routes(start_city: str, end_city: str, top_n: int = 5) -> list:
    return find_optimal_routes(start_city, end_city, 'time_min', top_n)


def find_most_comfortable_routes(start_city: str, end_city: str, top_n: int = 5) -> list:
    return find_optimal_routes(start_city, end_city, 'comfort', top_n, reverse=True)


def find_optimal_routes(start_city: str, end_city: str, criterion: str, top_n: int, reverse: bool = False) -> list:
    '''

    :param start_city:
    :param end_city:
    :param criterion: time_min/cost/comfort
    :param top_n:
    :param reverse:
    :return:
    '''
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row

    try:
        start_id = conn.execute("SELECT id FROM cities WHERE name = ?", (start_city,)).fetchone()
        end_id = conn.execute("SELECT id FROM cities WHERE name = ?", (end_city,)).fetchone()

        if not start_id or not end_id:
            return []

        start_id = start_id['id']
        end_id = end_id['id']

        graph = defaultdict(dict)
        cursor = conn.cursor()
        multiplier = -1 if (criterion == 'comfort' and reverse) else 1

        cursor.execute(f"SELECT from_city_id, to_city_id, {criterion} as weight FROM routes")
        for row in cursor:
            graph[row['from_city_id']][row['to_city_id']] = row['weight'] * multiplier

        heap = []
        heapq.heappush(heap, (0, [start_id]))
        found_routes = []

        while heap and len(found_routes) < top_n:
            current_cost, path = heapq.heappop(heap)
            last_node = path[-1]

            if last_node == end_id:
                route_info = get_route_details(conn, path)
                found_routes.append(route_info)
                continue

            for neighbor, cost in graph[last_node].items():
                if neighbor not in path:
                    new_path = path + [neighbor]
                    new_cost = current_cost + cost
                    heapq.heappush(heap, (new_cost, new_path))

        return found_routes
    finally:
        conn.close()


def get_route_details(conn, path):
    route = {
        'path': [],
        'transport': [],
        'total_cost': 0,
        'total_time': 0,
        'total_comfort': 0,
        'segments': []
    }

    cursor = conn.cursor()

    for i in range(len(path) - 1):
        from_id, to_id = path[i], path[i + 1]

        cursor.execute("""
                       SELECT c1.name as from_city,
                              c2.name as to_city,
                              transport_type,
                              cost,
                              time_min,
                              comfort
                       FROM routes
                                JOIN cities c1 ON from_city_id = c1.id
                                JOIN cities c2 ON to_city_id = c2.id
                       WHERE from_city_id = ?
                         AND to_city_id = ?
                       """, (from_id, to_id))

        segment = cursor.fetchone()

        route['path'].append(segment['from_city'])
        route['transport'].append(segment['transport_type'])
        route['total_cost'] += segment['cost']
        route['total_time'] += segment['time_min']
        route['total_comfort'] += segment['comfort']

        route['segments'].append({
            'from': segment['from_city'],
            'to': segment['to_city'],
            'transport': segment['transport_type'],
            'cost': segment['cost'],
            'time': segment['time_min'],
            'comfort': segment['comfort']
        })

    cursor.execute("SELECT name FROM cities WHERE id = ?", (path[-1],))
    route['path'].append(cursor.fetchone()['name'])

    if route['segments']:
        route['avg_comfort'] = route['total_comfort'] / len(route['segments'])

    return route
