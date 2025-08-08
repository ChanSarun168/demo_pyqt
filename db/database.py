import sqlite3

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_user_table()
        self._create_question_table()
        self.seed_questions()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)

    # ---------- USER TABLE ----------
    def _create_user_table(self):
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

    # ---------- QUESTIONS TABLE ----------
    def _create_question_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def seed_questions(self):
        cursor = self.conn.cursor()

        sample_questions = [
            ("What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", "Paris"),
            ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "Mars"),
            ("What is 2 + 2?", "3", "4", "5", "6", "4"),
            ("Which gas do plants use for photosynthesis?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", "Carbon Dioxide"),
            ("Who wrote 'Romeo and Juliet'?", "Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen", "William Shakespeare"),
            ("What is the largest ocean on Earth?", "Atlantic", "Pacific", "Indian", "Arctic", "Pacific"),
            ("Which country is famous for the Great Wall?", "India", "China", "Japan", "Korea", "China"),
            ("What is the boiling point of water?", "90°C", "100°C", "110°C", "120°C", "100°C"),
            ("What is the currency of Japan?", "Yuan", "Yen", "Won", "Dollar", "Yen"),
            ("Which element has the chemical symbol 'O'?", "Oxygen", "Gold", "Silver", "Osmium", "Oxygen")
        ]

        cursor.executemany('''
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_questions)

        self.conn.commit()

    def get_all_questions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM questions")
        return cursor.fetchall()

    # ---------- CLOSE CONNECTION ----------
    def close(self):
        if self.conn:
            self.conn.close()
