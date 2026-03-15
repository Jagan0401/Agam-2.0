import sqlite3
import json

def check_props():
    conn = sqlite3.connect('agam.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, tags FROM properties")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Tags: {row[2]}")
    conn.close()

if __name__ == "__main__":
    check_props()
