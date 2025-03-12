import sqlite3

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None  # Explicitly declare cursor
    
    def _connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()  # Create cursor here
    
    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS summaries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  url TEXT UNIQUE,
                  date TEXT,
                  duration INTEGER,
                  channel_name TEXT,
                  summary TEXT)'''
        self.cursor.execute(sql)
        self.conn.commit()

    def store_summary(self, summary, metadata):
        """Store video summary and metadata in the database."""
        sql = '''INSERT INTO summaries (title, url, date, duration, channel_name, summary)
                 VALUES (?, ?, ?, ?, ?, ?)'''
        values = (metadata['title'], metadata['url'], metadata['date'], metadata['duration'], metadata['channel_name'], summary)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close_connection(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
