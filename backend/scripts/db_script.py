import sqlite3
import random
from pathlib import Path

db_path = Path('../app/data/database.db')
if db_path.exists():
    db_path.unlink()

conn = sqlite3.connect('../app/data/database.db')
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE cities
               (
                   id        INTEGER PRIMARY KEY AUTOINCREMENT,
                   name      TEXT NOT NULL UNIQUE,
                   latitude  REAL,
                   longitude REAL
               );
               """)

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
               );
               """)

cities = [
    ('Москва', 55.7558, 37.6176),
    ('Санкт-Петербург', 59.9343, 30.3351),
    ('Казань', 55.7963, 49.1088),
    ('Новосибирск', 55.0084, 82.9357),
    ('Екатеринбург', 56.8389, 60.6057),
    ('Нижний Новгород', 56.2965, 43.9361),
    ('Челябинск', 55.1644, 61.4368),
    ('Самара', 53.1959, 50.1002),
    ('Омск', 54.9914, 73.3645),
    ('Ростов-на-Дону', 47.2357, 39.7015),
    ('Уфа', 54.7388, 55.9721),
    ('Красноярск', 56.0087, 92.8705),
    ('Пермь', 58.0105, 56.2294),
    ('Воронеж', 51.672, 39.1843),
    ('Волгоград', 48.7071, 44.517),
    ('Краснодар', 45.0355, 38.9753),
    ('Саратов', 51.5924, 45.9608),
    ('Тюмень', 57.153, 65.5343),
    ('Тольятти', 53.5085, 49.4181),
    ('Ижевск', 56.8527, 53.2115),
    ('Барнаул', 53.3561, 83.7496),
    ('Ульяновск', 54.3142, 48.4031),
    ('Иркутск', 52.2864, 104.2807),
    ('Хабаровск', 48.4802, 135.0719),
    ('Ярославль', 57.6261, 39.8845),
    ('Владивосток', 43.1155, 131.8855),
    ('Махачкала', 42.9849, 47.5047),
    ('Томск', 56.4846, 84.9476),
    ('Оренбург', 51.7682, 55.097),
    ('Кемерово', 55.3547, 86.0873),
    ('Новокузнецк', 53.7865, 87.1552),
    ('Рязань', 54.6294, 39.7417),
    ('Астрахань', 46.3479, 48.0336),
    ('Набережные Челны', 55.7436, 52.3958),
    ('Пенза', 53.195, 45.0183),
    ('Липецк', 52.6088, 39.5992),
    ('Киров', 58.6036, 49.668),
    ('Чебоксары', 56.1439, 47.2489),
    ('Тула', 54.193, 37.6173),
    ('Калининград', 54.7104, 20.4522),
    ('Балашиха', 55.8094, 37.9581),
    ('Курск', 51.7304, 36.1926),
    ('Ставрополь', 45.0445, 41.9691),
    ('Улан-Удэ', 51.8335, 107.5841),
    ('Сочи', 43.5855, 39.7231),
    ('Брянск', 53.2436, 34.3634),
    ('Сургут', 61.254, 73.3962),
    ('Владимир', 56.129, 40.407),
    ('Архангельск', 64.5393, 40.5187),
    ('Чита', 52.0339, 113.4993),
    ('Симферополь', 44.9521, 34.1024)
]

cursor.executemany(
    "INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
    cities
)

transport_types = ['plane', 'train', 'bus', 'car']
routes = []

for _ in range(1200):
    from_id = random.randint(1, 50)
    to_id = random.randint(1, 50)

    while from_id == to_id:
        to_id = random.randint(1, 50)

    transport = random.choice(transport_types)
    cost = random.randint(500, 10500)
    time_min = random.randint(60, 660)
    comfort = random.randint(40, 100)
    accessibility = random.randint(0, 1)

    routes.append((from_id, to_id, transport, cost, time_min, comfort, accessibility))

cursor.executemany(
    """INSERT INTO routes
       (from_city_id, to_city_id, transport_type, cost, time_min, comfort, accessibility)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    routes
)

conn.commit()
conn.close()