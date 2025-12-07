"""
Migration script to add profile fields to existing students table.
Run this once to update your existing database.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'students.db')

def migrate():
    """Add new profile fields to students table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(students)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add new columns if they don't exist
    new_columns = {
        'grade': 'TEXT',
        'section': 'TEXT',
        'age': 'INTEGER',
        'gender': 'TEXT',
        'email': 'TEXT',
        'phone': 'TEXT',
        'address': 'TEXT'
    }
    
    for column_name, column_type in new_columns.items():
        if column_name not in columns:
            try:
                cursor.execute(f'ALTER TABLE students ADD COLUMN {column_name} {column_type}')
                print(f"✓ Added column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"✗ Column {column_name} already exists or error: {e}")
    
    conn.commit()
    conn.close()
    print("\n✅ Migration completed successfully!")

if __name__ == '__main__':
    print("Starting database migration to add profile fields...")
    migrate()
