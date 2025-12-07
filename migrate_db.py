"""
Database migration script to add exam_name column to exams table.
Run this if you have existing data.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'students.db')

def migrate_database():
    """Add exam_name column to existing exams table."""
    if not os.path.exists(DB_PATH):
        print("No existing database found. Schema will be created on first run.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(exams)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'exam_name' not in columns:
        print("Adding exam_name column to exams table...")
        cursor.execute("ALTER TABLE exams ADD COLUMN exam_name TEXT DEFAULT 'General'")
        conn.commit()
        print("✅ Migration complete!")
    else:
        print("✅ Database already up to date.")
    
    conn.close()

if __name__ == '__main__':
    migrate_database()
