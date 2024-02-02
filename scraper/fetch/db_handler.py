import sqlite3
import hashlib
import os

class DbHandler:
    # Constants for configuration
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'news.db')

    def __init__(self):
        self.conn = sqlite3.connect(DbHandler.DATABASE_PATH)
        self.create_table()

    def create_table(self):
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS entries
                                (id TEXT PRIMARY KEY,
                                  site TEXT,
                                  title TEXT,
                                  content TEXT,
                                  author TEXT,
                                  src TEXT,
                                  date TEXT)''')
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def save_entry(self, site, title, content, author, src, date):
        cursor = self.conn.cursor()
        id = hashlib.md5(src.encode('utf-8')).hexdigest()
        cursor.execute("SELECT * FROM entries WHERE id = ?", (id,))
        if cursor.fetchone():
            # Update existing entry
            cursor.execute('''UPDATE entries SET site = ?, title = ?, content = ?,
                              author = ?, src = ?, date = ? WHERE id = ?''',
                            (site, title, content, author, src, date, id))
        else:
            # Insert new entry
            cursor.execute('''INSERT INTO entries (id, site, title, content, author, src, date)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (id, site, title, content, author, src, date))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
