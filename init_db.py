import sqlite3

conn = sqlite3.connect("urls.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    short_code TEXT PRIMARY KEY,
    long_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Database initialized")
