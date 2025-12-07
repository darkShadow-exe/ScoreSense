import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'students.db')

def init_db():
    """Initialize the database with required tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            marks TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL,
            exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

def add_student(name, marks_dict):
    """
    Add a new student with marks.
    Args:
        name: Student name
        marks_dict: Dictionary of subject: score pairs
    Returns:
        Student ID if successful, None if student exists
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        marks_json = json.dumps(marks_dict)
        cursor.execute('INSERT INTO students (name, marks) VALUES (?, ?)', (name, marks_json))
        
        student_id = cursor.lastrowid
        
        # Also add to exams table for tracking history
        for subject, score in marks_dict.items():
            cursor.execute('INSERT INTO exams (student_id, subject, score) VALUES (?, ?, ?)',
                         (student_id, subject, float(score)))
        
        conn.commit()
        conn.close()
        return student_id
    except sqlite3.IntegrityError:
        return None

def get_all_students():
    """Get all students with their marks."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, marks FROM students ORDER BY name')
    rows = cursor.fetchall()
    
    students = []
    for row in rows:
        students.append({
            'id': row[0],
            'name': row[1],
            'marks': json.loads(row[2])
        })
    
    conn.close()
    return students

def get_student_by_id(student_id):
    """Get a specific student by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, marks FROM students WHERE id = ?', (student_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'marks': json.loads(row[2])
        }
    return None

def get_student_by_name(name):
    """Get a specific student by name."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, marks FROM students WHERE LOWER(name) = LOWER(?)', (name,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'marks': json.loads(row[2])
        }
    return None

def update_student(student_id, name=None, marks_dict=None):
    """Update student information."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if name:
        cursor.execute('UPDATE students SET name = ? WHERE id = ?', (name, student_id))
    
    if marks_dict:
        marks_json = json.dumps(marks_dict)
        cursor.execute('UPDATE students SET marks = ? WHERE id = ?', (marks_json, student_id))
        
        # Add new exam records
        for subject, score in marks_dict.items():
            cursor.execute('INSERT INTO exams (student_id, subject, score) VALUES (?, ?, ?)',
                         (student_id, subject, float(score)))
    
    conn.commit()
    conn.close()
    return True

def delete_student(student_id):
    """Delete a student and their exam records."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM exams WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    
    conn.commit()
    conn.close()
    return True

def get_student_history(student_id, subject):
    """Get historical scores for a student in a specific subject."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT score, exam_date 
        FROM exams 
        WHERE student_id = ? AND subject = ?
        ORDER BY exam_date
    ''', (student_id, subject))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{'score': row[0], 'date': row[1]} for row in rows]

def get_all_subjects():
    """Get list of all unique subjects."""
    students = get_all_students()
    subjects = set()
    
    for student in students:
        subjects.update(student['marks'].keys())
    
    return sorted(list(subjects))

# Initialize database on import
init_db()
