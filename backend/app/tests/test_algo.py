import pytest
import asyncio
import sqlite3
from backend.app.functions.routes import initialize, find_routes_async


def sync_init(db_path):
    asyncio.run(initialize(db_path))


def sync_find_routes(*args, **kwargs):
    return asyncio.run(find_routes_async(*args, **kwargs))


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE cities(id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("""CREATE TABLE routes
                      (
                          from_city_id   INTEGER,
                          to_city_id     INTEGER,
                          cost           REAL,
                          time_min       INTEGER,
                          comfort        REAL,
                          transport_type TEXT
                      )""")

    cursor.executemany(
        "INSERT INTO cities VALUES(?, ?)",
        [(1, "Moscow"), (2, "SPb"), (3, "Kazan")]
    )

    cursor.executemany(
        "INSERT INTO routes VALUES(?, ?, ?, ?, ?, ?)",
        [
            (1, 2, 100, 60, 0.8, "train"),
            (2, 3, 150, 90, 0.7, "bus"),
            (1, 3, 200, 120, 0.9, "plane")
        ]
    )

    conn.commit()
    conn.close()
    return db_path

def test_find_routes(test_db):
    sync_init(test_db)

    routes = sync_find_routes("Moscow", "Kazan", "cost")
    assert len(routes) > 0
    assert routes[0]["total_cost"] == 200

    routes = sync_find_routes("Moscow", "Kazan", "time_min")
    assert routes[0]["total_time"] == 120


    routes = sync_find_routes("Unknown", "Kazan", "cost")
    assert len(routes) == 0


@pytest.mark.parametrize("city_from,city_to,expected_cost", [
    ("Moscow", "SPb", 100),
    ("SPb", "Kazan", 150),
    ("Moscow", "Kazan", 200)
])
def test_route_costs(test_db, city_from, city_to, expected_cost):
    sync_init(test_db)
    routes = sync_find_routes(city_from, city_to, "cost")
    assert routes[0]["total_cost"] == expected_cost