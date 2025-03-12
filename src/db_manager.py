# src/db_manager.py
import sqlite3

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                date TEXT,
                duration TEXT,
                channel_name TEXT,
                summary TEXT
            )
        ''')
        self.conn.commit()

    def close_connection(self):  # good practice
        self.conn.close()
