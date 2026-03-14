import sqlite3
import os

def sync_database_schema():
    db_path = "agam.db"
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Columns to check/add in 'properties' table
    columns_to_add = [
        ("moderation_status", "TEXT DEFAULT 'approved'"),
        ("moderation_reason", "TEXT DEFAULT ''"),
        ("report_count", "INTEGER DEFAULT 0"),
        ("gallery", "TEXT DEFAULT '[]'"),
        ("created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("processed_at", "DATETIME")
    ]

    # Get current columns
    cursor.execute("PRAGMA table_info(properties)")
    current_columns = [col[1] for col in cursor.fetchall()]

    for col_name, col_def in columns_to_add:
        if col_name not in current_columns:
            print(f"Adding missing column '{col_name}' to properties table...")
            try:
                cursor.execute(f"ALTER TABLE properties ADD COLUMN {col_name} {col_def}")
            except Exception as e:
                print(f"Error adding column {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Database sync complete.")

if __name__ == "__main__":
    sync_database_schema()
