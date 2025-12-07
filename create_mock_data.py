"""
Create comprehensive mock database with 25+ students and full exam data.
Clears existing database and populates with realistic data.
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta

# Database path
DB_PATH = 'db/students.db'

# Student data
FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'William', 'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia',
    'Lucas', 'Harper', 'Henry', 'Evelyn', 'Alexander', 'Abigail', 'Michael',
    'Emily', 'Daniel', 'Elizabeth', 'Matthew', 'Sofia', 'Joseph', 'Avery',
    'David', 'Ella', 'Jackson', 'Scarlett', 'Logan', 'Grace'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
    'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
    'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark'
]

GRADES = ['9', '10', '11', '12']
SECTIONS = ['A', 'B', 'C', 'D']
GENDERS = ['Male', 'Female']

# Subject configuration
SUBJECTS = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Computer Science']
EXAM_NAMES = ['First Term', 'Midterm', 'Pre-Finals', 'Finals']

def clear_database():
    """Remove existing database file."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✓ Cleared existing database")

def create_database():
    """Create fresh database with schema."""
    os.makedirs('db', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            marks TEXT,
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
    
    # Create exams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            exam_name TEXT,
            subject TEXT,
            score REAL,
            exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Created database schema")

def generate_student_data(count=30):
    """Generate realistic student data."""
    students = []
    used_names = set()
    
    for i in range(count):
        # Generate unique name
        while True:
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        # Generate profile
        grade = random.choice(GRADES)
        section = random.choice(SECTIONS)
        age = int(grade) + 5 + random.randint(0, 1)  # Age roughly matches grade
        gender = random.choice(GENDERS)
        email = f"{first_name.lower()}.{last_name.lower()}@school.edu"
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        address = f"{random.randint(100, 9999)} {random.choice(['Oak', 'Maple', 'Pine', 'Elm', 'Cedar'])} Street, {random.choice(['Springfield', 'Riverside', 'Greenwood', 'Lakeside'])}"
        
        students.append({
            'name': full_name,
            'grade': grade,
            'section': section,
            'age': age,
            'gender': gender,
            'email': email,
            'phone': phone,
            'address': address
        })
    
    return students

def generate_exam_scores(student_id, base_ability):
    """
    Generate realistic exam scores for a student.
    base_ability: 0.0 to 1.0 indicating student's overall capability
    """
    exams = []
    
    # Each student's strength varies by subject
    subject_strengths = {
        subject: base_ability + random.uniform(-0.15, 0.15)
        for subject in SUBJECTS
    }
    
    # Clamp strengths between 0.3 and 1.0
    for subject in subject_strengths:
        subject_strengths[subject] = max(0.3, min(1.0, subject_strengths[subject]))
    
    # Generate scores for each exam
    for exam_idx, exam_name in enumerate(EXAM_NAMES):
        for subject in SUBJECTS:
            # Base score from student's strength in subject
            strength = subject_strengths[subject]
            base_score = 50 + (strength * 40)  # 50-90 range based on strength
            
            # Add improvement trend (students generally improve over time)
            improvement = exam_idx * random.uniform(0, 5)
            
            # Add random variation (±10 points)
            variation = random.uniform(-10, 10)
            
            # Calculate final score
            score = base_score + improvement + variation
            
            # Clamp between 40 and 100
            score = max(40, min(100, score))
            score = round(score, 1)
            
            exams.append({
                'student_id': student_id,
                'exam_name': exam_name,
                'subject': subject,
                'score': score
            })
    
    return exams

def populate_database():
    """Populate database with mock data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Generate students
    students = generate_student_data(30)
    print(f"✓ Generated {len(students)} student profiles")
    
    # Insert students and their exams
    total_exams = 0
    for student in students:
        # Insert student
        cursor.execute('''
            INSERT INTO students (name, marks, grade, section, age, gender, email, phone, address)
            VALUES (?, '{}', ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student['name'],
            student['grade'],
            student['section'],
            student['age'],
            student['gender'],
            student['email'],
            student['phone'],
            student['address']
        ))
        
        student_id = cursor.lastrowid
        
        # Generate base ability for this student (0.4 to 0.95)
        base_ability = random.uniform(0.4, 0.95)
        
        # Generate and insert exams
        exams = generate_exam_scores(student_id, base_ability)
        for exam in exams:
            cursor.execute('''
                INSERT INTO exams (student_id, exam_name, subject, score, exam_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                exam['student_id'],
                exam['exam_name'],
                exam['subject'],
                exam['score'],
                datetime.now() - timedelta(days=random.randint(1, 180))
            ))
            total_exams += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ Inserted {len(students)} students")
    print(f"✓ Inserted {total_exams} exam records")
    print(f"✓ Average of {total_exams // len(students)} exams per student")

def verify_database():
    """Verify database contents."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count students
    cursor.execute('SELECT COUNT(*) FROM students')
    student_count = cursor.fetchone()[0]
    
    # Count exams
    cursor.execute('SELECT COUNT(*) FROM exams')
    exam_count = cursor.fetchone()[0]
    
    # Get sample student
    cursor.execute('''
        SELECT s.name, s.grade, s.section, COUNT(e.id) as exam_count
        FROM students s
        LEFT JOIN exams e ON s.id = e.student_id
        GROUP BY s.id
        LIMIT 5
    ''')
    samples = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "="*60)
    print("DATABASE VERIFICATION")
    print("="*60)
    print(f"Total Students: {student_count}")
    print(f"Total Exam Records: {exam_count}")
    print(f"\nSample Students:")
    for name, grade, section, exams in samples:
        print(f"  • {name} (Grade {grade}-{section}): {exams} exam records")
    print("="*60)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CREATING COMPREHENSIVE MOCK DATABASE")
    print("="*60 + "\n")
    
    clear_database()
    create_database()
    populate_database()
    verify_database()
    
    print("\n✅ Mock database created successfully!")
    print("Run 'python app.py' to start the application.\n")
