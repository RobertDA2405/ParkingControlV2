import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bdparqueo"
    )

class Database:
    @staticmethod
    def get_connection():
        return connect_db()

    def __init__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
