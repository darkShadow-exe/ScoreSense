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
            exam_name TEXT DEFAULT 'General',
            exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

def add_student(name, marks_dict, exam_name='Initial'):
    """
    Add a new student with marks.
    Args:
        name: Student name
        marks_dict: Dictionary of subject: score pairs
        exam_name: Name of the exam/test
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
            cursor.execute('INSERT INTO exams (student_id, subject, score, exam_name) VALUES (?, ?, ?, ?)',
                         (student_id, subject, float(score), exam_name))
        
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

def update_student(student_id, name=None, marks_dict=None, exam_name='Update'):
    """Update student information and add new exam scores."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if name:
        cursor.execute('UPDATE students SET name = ? WHERE id = ?', (name, student_id))
    
    if marks_dict:
        marks_json = json.dumps(marks_dict)
        cursor.execute('UPDATE students SET marks = ? WHERE id = ?', (marks_json, student_id))
        
        # Add new exam records
        for subject, score in marks_dict.items():
            cursor.execute('INSERT INTO exams (student_id, subject, score, exam_name) VALUES (?, ?, ?, ?)',
                         (student_id, subject, float(score), exam_name))
    
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
        SELECT score, exam_date, exam_name 
        FROM exams 
        WHERE student_id = ? AND subject = ?
        ORDER BY exam_date
    ''', (student_id, subject))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{'score': row[0], 'date': row[1], 'exam_name': row[2]} for row in rows]

def get_all_exams_for_student(student_id):
    """Get all exams for a student grouped by subject."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, subject, score, exam_name, exam_date 
        FROM exams 
        WHERE student_id = ?
        ORDER BY subject, exam_date DESC
    ''', (student_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    exams_by_subject = {}
    for row in rows:
        subject = row[1]
        if subject not in exams_by_subject:
            exams_by_subject[subject] = []
        exams_by_subject[subject].append({
            'id': row[0],
            'score': row[2],
            'exam_name': row[3],
            'date': row[4]
        })
    
    return exams_by_subject

def get_exams_grouped_by_name(student_id):
    """Get all exams for a student grouped by exam name."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, subject, score, exam_name, exam_date 
        FROM exams 
        WHERE student_id = ?
        ORDER BY exam_date DESC, exam_name, subject
    ''', (student_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    exams_by_name = {}
    for row in rows:
        exam_name = row[3]
        if exam_name not in exams_by_name:
            exams_by_name[exam_name] = {
                'date': row[4],
                'subjects': []
            }
        exams_by_name[exam_name]['subjects'].append({
            'id': row[0],
            'subject': row[1],
            'score': row[2]
        })
    
    return exams_by_name

def add_complete_exam(student_id, exam_name, marks_dict):
    """Add a complete exam with multiple subjects at once."""
    conn = get_connection()
    cursor = conn.cursor()
    
    for subject, score in marks_dict.items():
        cursor.execute('INSERT INTO exams (student_id, subject, score, exam_name) VALUES (?, ?, ?, ?)',
                     (student_id, subject, float(score), exam_name))
    
    # Update the student's current marks with latest scores
    student = get_student_by_id(student_id)
    if student:
        student['marks'].update(marks_dict)
        marks_json = json.dumps(student['marks'])
        cursor.execute('UPDATE students SET marks = ? WHERE id = ?', (marks_json, student_id))
    
    conn.commit()
    conn.close()
    return True

def get_student_detailed_stats(student_id):
    """Get comprehensive statistics for a specific student."""
    from utils.stats import calculate_stats, get_trend
    
    student = get_student_by_id(student_id)
    if not student:
        return None
    
    exams_by_subject = get_all_exams_for_student(student_id)
    exams_by_name = get_exams_grouped_by_name(student_id)
    
    # Calculate stats per subject
    subject_stats = {}
    for subject, exams in exams_by_subject.items():
        scores = [exam['score'] for exam in exams]
        if scores:
            subject_stats[subject] = {
                'average': sum(scores) / len(scores),
                'highest': max(scores),
                'lowest': min(scores),
                'trend': get_trend(scores),
                'exam_count': len(scores),
                'latest': scores[0] if scores else 0
            }
    
    # Overall stats
    all_scores = []
    for subject_exams in exams_by_subject.values():
        all_scores.extend([exam['score'] for exam in subject_exams])
    
    overall_stats = {}
    if all_scores:
        overall_stats = {
            'average': sum(all_scores) / len(all_scores),
            'highest': max(all_scores),
            'lowest': min(all_scores),
            'total_exams': len(all_scores),
            'subjects_count': len(exams_by_subject)
        }
    
    return {
        'student': student,
        'exams_by_subject': exams_by_subject,
        'exams_by_name': exams_by_name,
        'subject_stats': subject_stats,
        'overall_stats': overall_stats
    }

def add_exam_score(student_id, subject, score, exam_name='Test'):
    """Add a new exam score for a student."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO exams (student_id, subject, score, exam_name) VALUES (?, ?, ?, ?)',
                 (student_id, subject, float(score), exam_name))
    
    # Update the student's current marks
    student = get_student_by_id(student_id)
    if student:
        student['marks'][subject] = float(score)
        marks_json = json.dumps(student['marks'])
        cursor.execute('UPDATE students SET marks = ? WHERE id = ?', (marks_json, student_id))
    
    conn.commit()
    conn.close()
    return True

def delete_exam(exam_id):
    """Delete a specific exam record."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
    
    conn.commit()
    conn.close()
    return True

def get_all_subjects():
    """Get list of all unique subjects."""
    students = get_all_students()
    subjects = set()
    
    for student in students:
        subjects.update(student['marks'].keys())
    
    return sorted(list(subjects))

# Initialize database on import
init_db()
