from models.student_model import get_all_students, get_all_subjects
import statistics
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'students.db')

def get_connection():
    """Get a database connection with timeout and autocommit."""
    # Use isolation_level=None for autocommit mode to prevent locks
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    return conn

def get_class_average():
    """Calculate overall class average across all subjects from exams table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT AVG(score) FROM exams')
    result = cursor.fetchone()[0]
    conn.close()
    
    return round(result, 2) if result else 0

def get_subject_averages():
    """Calculate average score for each subject from exams table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT subject, AVG(score) as avg_score
        FROM exams
        GROUP BY subject
        ORDER BY subject
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    averages = {}
    for row in rows:
        averages[row[0]] = round(row[1], 2)
    
    return averages

def get_class_topper(subject=None):
    """
    Get the student with highest score.
    If subject is specified, get topper for that subject.
    Otherwise, get overall topper based on average.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if subject:
        # Subject-specific topper from exams table
        cursor.execute('''
            SELECT s.name, e.score
            FROM students s
            JOIN exams e ON s.id = e.student_id
            WHERE e.subject = ?
            ORDER BY e.score DESC
            LIMIT 1
        ''', (subject,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'name': row[0],
                'score': round(row[1], 2),
                'subject': subject
            }
        return None
    else:
        # Overall topper based on average from exams table
        cursor.execute('''
            SELECT s.name, AVG(e.score) as avg_score
            FROM students s
            JOIN exams e ON s.id = e.student_id
            GROUP BY s.id, s.name
            ORDER BY avg_score DESC
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'name': row[0],
                'average': round(row[1], 2)
            }
        return None

def get_lowest_scorer(subject=None):
    """Get the student with lowest score from exams table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if subject:
        # Subject-specific lowest from exams table
        cursor.execute('''
            SELECT s.name, e.score
            FROM students s
            JOIN exams e ON s.id = e.student_id
            WHERE e.subject = ?
            ORDER BY e.score ASC
            LIMIT 1
        ''', (subject,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'name': row[0],
                'score': round(row[1], 2),
                'subject': subject
            }
        return None
    else:
        # Overall lowest based on average from exams table
        cursor.execute('''
            SELECT s.name, AVG(e.score) as avg_score
            FROM students s
            JOIN exams e ON s.id = e.student_id
            GROUP BY s.id, s.name
            ORDER BY avg_score ASC
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'name': row[0],
                'average': round(row[1], 2)
            }
        return None

def get_subject_difficulty():
    """
    Rank subjects by difficulty (lower average = more difficult).
    Returns list of tuples (subject, average) sorted by difficulty.
    """
    averages = get_subject_averages()
    
    # Sort by average (ascending = most difficult first)
    difficulty_ranking = sorted(averages.items(), key=lambda x: x[1])
    
    return difficulty_ranking

def get_student_rank(student_name):
    """Get rank of a student based on overall average from exams table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all students with their averages from exams table
    cursor.execute('''
        SELECT s.name, AVG(e.score) as avg_score
        FROM students s
        LEFT JOIN exams e ON s.id = e.student_id
        GROUP BY s.id, s.name
        ORDER BY avg_score DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return None
    
    # Build list of students with averages
    student_averages = []
    for row in rows:
        avg = row[1] if row[1] else 0
        student_averages.append({
            'name': row[0],
            'average': avg
        })
    
    # Already sorted by average DESC
    # Find rank
    for rank, student in enumerate(student_averages, 1):
        if student['name'].lower() == student_name.lower():
            return {
                'rank': rank,
                'total': len(student_averages),
                'average': round(student['average'], 2)
            }
    
    return None

def get_score_distribution():
    """Get distribution of scores in ranges from exams table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT score FROM exams')
    rows = cursor.fetchall()
    conn.close()
    
    ranges = {
        '0-40': 0,
        '41-60': 0,
        '61-80': 0,
        '81-100': 0
    }
    
    for row in rows:
        score = row[0]
        if score <= 40:
            ranges['0-40'] += 1
        elif score <= 60:
            ranges['41-60'] += 1
        elif score <= 80:
            ranges['61-80'] += 1
        else:
            ranges['81-100'] += 1
    
    return ranges

def get_all_stats():
    """Get comprehensive statistics."""
    students = get_all_students()
    
    if not students:
        return {
            'total_students': 0,
            'class_average': 0,
            'subject_averages': {},
            'topper': None,
            'lowest': None,
            'difficulty_ranking': []
        }
    
    return {
        'total_students': len(students),
        'class_average': get_class_average(),
        'subject_averages': get_subject_averages(),
        'topper': get_class_topper(),
        'lowest': get_lowest_scorer(),
        'difficulty_ranking': get_subject_difficulty(),
        'score_distribution': get_score_distribution()
    }

def compare_subject_scores(subject):
    """Get all students' scores in a specific subject for comparison from exams table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.name, AVG(e.score) as avg_score
        FROM students s
        JOIN exams e ON s.id = e.student_id
        WHERE e.subject = ?
        GROUP BY s.id, s.name
        ORDER BY avg_score DESC
    ''', (subject,))
    
    rows = cursor.fetchall()
    conn.close()
    
    comparisons = []
    for row in rows:
        comparisons.append({
            'name': row[0],
            'score': round(row[1], 2)
        })
    
    return comparisons
