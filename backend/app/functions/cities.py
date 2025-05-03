import sqlite3

path_db = './app/data/database.db'

def get_cities() -> list:
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cities = cursor.execute('''
    SELECT name FROM cities;
                            ''').fetchall()
    conn.close()
    cities = [i[0] for i in cities]
    return cities