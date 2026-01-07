#!/usr/bin/env python3
"""
Database Reset Script for ScoreSense
Deletes all data from the database while preserving table structure.
Use this to reset the database to a clean state for demos or testing.
"""

import sqlite3
import os
import sys

def get_database_path():
    """Get the path to the database file."""
    # Check the actual location used by the app
    db_folder_path = os.path.join('db', 'students.db')
    if os.path.exists(db_folder_path):
        return db_folder_path
    
    # Check if running from the project root
    if os.path.exists('students.db'):
        return 'students.db'
    
    # Check common locations
    possible_paths = [
        'database/students.db',
        'data/students.db',
        os.path.join(os.path.dirname(__file__), 'db', 'students.db'),
        os.path.join(os.path.dirname(__file__), 'students.db')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If not found, assume it's in the db directory
    return os.path.join('db', 'students.db')

def reset_database():
    """Delete all data from database tables while preserving structure."""
    db_path = get_database_path()
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        print("   Make sure you're running this script from the project directory.")
        return False
    
    print(f"🔍 Found database at: {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 Found {len(tables)} tables in database")
        
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Delete data from each table
        deleted_counts = {}
        for table_name in tables:
            table_name = table_name[0]
            
            # Skip sqlite internal tables
            if table_name.startswith('sqlite_'):
                continue
            
            # Count records before deletion
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count_before = cursor.fetchone()[0]
            
            # Delete all records
            cursor.execute(f"DELETE FROM {table_name}")
            deleted_counts[table_name] = count_before
            
            print(f"🗑️  Deleted {count_before} records from '{table_name}' table")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        print("🔄 Reset auto-increment counters")
        
        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Commit changes
        conn.commit()
        
        # Verify tables are empty
        print("\n✅ Verification:")
        for table_name in deleted_counts.keys():
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count_after = cursor.fetchone()[0]
            print(f"   '{table_name}' now has {count_after} records")
        
        conn.close()
        
        total_deleted = sum(deleted_counts.values())
        print(f"\n🎉 Database reset complete!")
        print(f"   Total records deleted: {total_deleted}")
        print(f"   Table structure preserved: ✅")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def confirm_reset():
    """Ask user for confirmation before deleting data."""
    print("⚠️  WARNING: This will delete ALL data from the ScoreSense database!")
    print("   - All student records will be removed")
    print("   - All exam scores will be removed") 
    print("   - All profile information will be removed")
    print("   - Table structure will be preserved")
    print()
    
    response = input("Are you sure you want to continue? (type 'YES' to confirm): ").strip()
    
    if response == 'YES':
        return True
    else:
        print("❌ Operation cancelled.")
        return False

def main():
    """Main function to handle database reset."""
    print("🗄️  ScoreSense Database Reset Utility")
    print("=" * 50)
    
    # Check if confirmation is needed
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        print("🔄 Force mode enabled - skipping confirmation")
        proceed = True
    else:
        proceed = confirm_reset()
    
    if proceed:
        print("\n🔄 Starting database reset...")
        success = reset_database()
        
        if success:
            print("\n✅ Database has been successfully reset!")
            print("   You can now run the application with a clean database.")
        else:
            print("\n❌ Database reset failed!")
            sys.exit(1)
    else:
        print("👋 No changes made. Database remains unchanged.")

if __name__ == '__main__':
    main()