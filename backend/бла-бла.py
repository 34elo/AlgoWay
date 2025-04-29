import sqlite3
from pathlib import Path


def create_database(db_path='./app/data/database.db'):
    """Создает базу данных с тестовыми данными"""
    # Удаляем старую базу, если существует
    if Path(db_path).exists():
        Path(db_path).unlink()

    # Подключаемся к базе
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу городов
    cursor.execute("""
                   CREATE TABLE cities
                   (
                       id        INTEGER PRIMARY KEY AUTOINCREMENT,
                       name      TEXT NOT NULL UNIQUE,
                       latitude  REAL,
                       longitude REAL
                   )
                   """)

    # Создаем таблицу маршрутов
    cursor.execute("""
                   CREATE TABLE routes
                   (
                       id             INTEGER PRIMARY KEY AUTOINCREMENT,
                       from_city_id   INTEGER NOT NULL,
                       to_city_id     INTEGER NOT NULL,
                       transport_type TEXT    NOT NULL CHECK (transport_type IN ('plane', 'train', 'bus', 'car')),
                       cost           REAL    NOT NULL CHECK (cost >= 0),
                       time_min       INTEGER NOT NULL CHECK (time_min > 0),
                       comfort        INTEGER NOT NULL CHECK (comfort BETWEEN 0 AND 100),
                       accessibility  INTEGER NOT NULL CHECK (accessibility IN (0, 1)),
                       FOREIGN KEY (from_city_id) REFERENCES cities (id),
                       FOREIGN KEY (to_city_id) REFERENCES cities (id)
                   )
                   """)

    # Создаем индексы
    cursor.execute("CREATE INDEX idx_routes_from ON routes(from_city_id)")
    cursor.execute("CREATE INDEX idx_routes_to ON routes(to_city_id)")
    cursor.execute("CREATE INDEX idx_routes_transport ON routes(transport_type)")

    # Добавляем тестовые города
    cities = [
        ('Москва', 55.7558, 37.6176),
        ('Санкт-Петербург', 59.9343, 30.3351),
        ('Казань', 55.7963, 49.1088),
        ('Сочи', 43.5855, 39.7231)
    ]
    cursor.executemany(
        "INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
        cities
    )

    # Добавляем тестовые маршруты
    routes = [
        # Москва - СПб
        (1, 2, 'plane', 5000, 90, 80, 1),
        (1, 2, 'train', 2500, 240, 70, 1),
        (1, 2, 'bus', 1500, 480, 50, 1),

        # Москва - Казань
        (1, 3, 'plane', 4000, 120, 75, 1),
        (1, 3, 'train', 1800, 540, 65, 1),

        # СПб - Казань
        (2, 3, 'plane', 4500, 150, 70, 1),

        # Москва - Сочи
        (1, 4, 'plane', 6000, 150, 85, 1),
        (1, 4, 'train', 3500, 1440, 75, 1),

        # СПб - Сочи
        (2, 4, 'plane', 6500, 180, 80, 1)
    ]
    cursor.executemany(
        """INSERT INTO routes
           (from_city_id, to_city_id, transport_type, cost, time_min, comfort, accessibility)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        routes
    )

    # Сохраняем изменения
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()