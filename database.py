import sqlite3

LOCATION_TYPES = [
     "region",
     "district",
     "city",
     "street",
     "address"
   ]

class Database:
    def __init__(self, path: str = 'locations.db'):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS locations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_type INTEGER,
            location_id INTEGER);
            """)
        self.conn.commit()

    def add_location(self, location: tuple):
        self.cur.execute("""
        INSERT INTO locations(location_type, location_id) 
           VALUES(?, ?);""", location)
        self.conn.commit()

    def show_table(self):
        self.cur.execute("SELECT * FROM locations;")
        result = self.cur.fetchall()
        for string in result:
            print(" ".join(map(str, string)))

    def get_location(self, id: int) -> tuple:
        self.cur.execute("select * from locations where id=?;", (id,))
        return self.cur.fetchone()

    def delete(self):
        self.cur.execute("""DROP TABLE locations""")
        self.conn.commit()


if __name__ == "__main__":
    database = Database()
    database.create_table()
    for i in range(0, 5):
        database.add_location((i, i))
    database.add_location((4, 4))
    database.add_location((3, 3))
    database.add_location((4, 7))
    database.add_location((2, 2))
    database.add_location((3, 9))
    database.add_location((4, 10))
    database.add_location((0, 0))
    for i in range(12, 16):
        database.add_location((i-11, i))
    database.show_table()
    #database.delete()
