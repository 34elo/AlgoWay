import sqlite3


if __name__ == '__main__':
    path_db = '../../data/database.db'
else:
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