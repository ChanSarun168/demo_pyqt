import sqlite3

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_table()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def validate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", 
            (username, password)
        )
        return cursor.fetchone()
    
    def register(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (username , password) VALUES(?,?)", 
            (username, password)
        )
        self.conn.commit()
        return True


    def close(self):
        if self.conn:
            self.conn.close()
