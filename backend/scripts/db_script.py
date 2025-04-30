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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    latitude REAL,
    longitude REAL
);
""")

cursor.execute("""
CREATE TABLE routes
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_city_id INTEGER NOT NULL,
    to_city_id INTEGER NOT NULL,
    transport_type TEXT NOT NULL CHECK (transport_type IN ('dragon', 'train', 'horse', 'boat')),
    cost REAL NOT NULL CHECK (cost >= 0),
    time_min INTEGER NOT NULL CHECK (time_min > 0),
    comfort INTEGER NOT NULL CHECK (comfort BETWEEN 0 AND 100),
    accessibility INTEGER NOT NULL CHECK (accessibility IN (0, 1)),
    FOREIGN KEY (from_city_id) REFERENCES fantasy_cities (id),
    FOREIGN KEY (to_city_id) REFERENCES fantasy_cities (id)
);
""")

fantasy_cities = [
    ('Златогорье', 10.5, 20.3),
    ('Березовка', 15.8, 30.1),
    ('Лукоморье', 20.7, 40.6),
    ('Тайница', 25.9, 50.2),
    ('Изумрудный город', 30.4, 60.5),
    ('Белогорье', 35.1, 70.8),
    ('Черняевка', 40.2, 80.7),
    ('Соловьиный край', 45.6, 90.3),
    ('Русь-Золотые Поля', 50.9, 100.1),
    ('Серебрянка', 55.3, 110.4),
    ('Драконье логово', 60.7, 120.6),
    ('Эльфийский лес', 65.2, 130.5),
    ('Тёмный лес', 70.8, 140.3),
    ('Гарнизон', 75.5, 150.7),
    ('Ривье', 80.1, 160.2),
    ('Мордор', 85.4, 170.6),
    ('Лориэн', 90.6, 180.5),
    ('Рохан', 95.3, 190.1),
    ('Гондор', 100.2, 200.4),
    ('Рив', 105.7, 210.6),
    ('Альквира', 110.5, 220.3),
    ('Каэр Морхен', 115.8, 230.1),
    ('Андора', 120.4, 240.7),
    ('Блэкхоллоу', 125.6, 250.2),
    ('Сияющий город', 130.3, 260.6),
    ('Сумеречье', 135.1, 270.5),
    ('Лунная долина', 140.8, 280.3),
    ('Звёздный пик', 145.5, 290.7),
    ('Теневой лес', 150.2, 300.1),
    ('Велесова пустошь', 155.7, 310.4),
    ('Поляна чудес', 160.5, 320.3),
    ('Дубрава', 165.8, 330.1),
    ('Залесье', 170.4, 340.7),
    ('Перелесок', 175.6, 350.2),
    ('Светлые холмы', 180.3, 360.6),
    ('Темнолесье', 185.1, 370.5),
    ('Кривое озеро', 190.8, 380.3),
    ('Липовый край', 195.5, 390.7),
    ('Рябиновый берег', 200.2, 400.1),
    ('Пихтовая гора', 205.7, 410.4),
    ('Еловая вершина', 210.5, 420.3),
    ('Берёзовая роща', 215.8, 430.1),
    ('Вязники', 220.4, 440.7),
    ('Кленовый лист', 225.6, 450.2),
    ('Тополиный тракт', 230.3, 460.6),
    ('Дубовая долина', 235.1, 470.5),
    ('Сосновый бор', 240.8, 480.3),
    ('Кедровая гора', 245.5, 490.7),
    ('Ельцовский край', 250.2, 500.1),
    ('Лесопарк', 255.7, 510.4),
    ('Зелёный луг', 260.5, 520.3),
    ('Цветущий сад', 265.8, 530.1),
    ('Солнечная поляна', 270.4, 540.7),
    ('Радужный берег', 275.6, 550.2),
    ('Искрящийся ручей', 280.3, 560.6),
    ('Весёлый лес', 285.1, 570.5),
    ('Сказочная долина', 290.8, 580.3),
    ('Волшебный холм', 295.5, 590.7)
]

cursor.executemany(
    "INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
    fantasy_cities
)

transport_types = ['dragon', 'train', 'horse', 'boat']
routes = []

for _ in range(3000):
    from_id = random.randint(1, len(fantasy_cities))
    to_id = random.randint(1, len(fantasy_cities))

    while from_id == to_id:
        to_id = random.randint(1, len(fantasy_cities))

    transport = random.choice(transport_types)
    cost = random.randint(500, 15000)
    time_min = random.randint(60, 720)
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