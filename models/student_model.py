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
            grade TEXT,
            section TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
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

def add_student(name, grade=None, section=None, age=None, gender=None, email=None, phone=None, address=None):
    """
    Add a new student with personal details only.
    Args:
        name: Student name
        grade: Grade/Class
        section: Section
        age: Age
        gender: Gender
        email: Email address
        phone: Phone number
        address: Address
    Returns:
        Student ID if successful, None if student exists
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Initialize with empty marks
        marks_json = json.dumps({})
        
        cursor.execute('''
            INSERT INTO students (name, marks, grade, section, age, gender, email, phone, address) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, marks_json, grade, section, age, gender, email, phone, address))
        
        student_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return student_id
    except sqlite3.IntegrityError:
        return None

def get_all_students():
    """Get all students with their marks and details."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, marks, grade, section, age, gender, email, phone, address FROM students ORDER BY name')
    rows = cursor.fetchall()
    
    students = []
    for row in rows:
        students.append({
            'id': row[0],
            'name': row[1],
            'marks': json.loads(row[2]),
            'grade': row[3],
            'section': row[4],
            'age': row[5],
            'gender': row[6],
            'email': row[7],
            'phone': row[8],
            'address': row[9]
        })
    
    conn.close()
    return students

def get_student_by_id(student_id):
    """Get a specific student by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, marks, grade, section, age, gender, email, phone, address FROM students WHERE id = ?', (student_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'marks': json.loads(row[2]),
            'grade': row[3],
            'section': row[4],
            'age': row[5],
            'gender': row[6],
            'email': row[7],
            'phone': row[8],
            'address': row[9]
        }
    return None

def get_student_by_name(name):
    """Get a specific student by name."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, marks, grade, section, age, gender, email, phone, address FROM students WHERE LOWER(name) = LOWER(?)', (name,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'marks': json.loads(row[2]),
            'grade': row[3],
            'section': row[4],
            'age': row[5],
            'gender': row[6],
            'email': row[7],
            'phone': row[8],
            'address': row[9]
        }
    return None

def update_student(student_id, name=None, grade=None, section=None, age=None, gender=None, email=None, phone=None, address=None, marks_dict=None, exam_name='Update'):
    """Update student information and optionally add new exam scores."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Update personal details
    update_fields = []
    update_values = []
    
    if name is not None:
        update_fields.append('name = ?')
        update_values.append(name)
    if grade is not None:
        update_fields.append('grade = ?')
        update_values.append(grade)
    if section is not None:
        update_fields.append('section = ?')
        update_values.append(section)
    if age is not None:
        update_fields.append('age = ?')
        update_values.append(age)
    if gender is not None:
        update_fields.append('gender = ?')
        update_values.append(gender)
    if email is not None:
        update_fields.append('email = ?')
        update_values.append(email)
    if phone is not None:
        update_fields.append('phone = ?')
        update_values.append(phone)
    if address is not None:
        update_fields.append('address = ?')
        update_values.append(address)
    
    if update_fields:
        update_values.append(student_id)
        cursor.execute(f'UPDATE students SET {", ".join(update_fields)} WHERE id = ?', update_values)
    
    # Add new exam records if marks provided
    if marks_dict:
        marks_json = json.dumps(marks_dict)
        cursor.execute('UPDATE students SET marks = ? WHERE id = ?', (marks_json, student_id))
        
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
