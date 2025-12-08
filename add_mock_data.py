"""
Comprehensive Mock Data Generator for ScoreSense
Generates realistic student data with multiple exams and subjects
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.student_model import add_student, add_complete_exam, get_all_students

# Configuration
NUM_STUDENTS = 30
SUBJECTS = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Geography', 'Computer Science']
EXAMS = ['Midterm', 'Final', 'Quiz 1', 'Quiz 2', 'Unit Test 1', 'Unit Test 2']
GRADES = ['9', '10', '11', '12']
SECTIONS = ['A', 'B', 'C']
GENDERS = ['Male', 'Female']

# Realistic first and last names
FIRST_NAMES_MALE = [
    'Aarav', 'Arjun', 'Rahul', 'Rohan', 'Karan', 'Aditya', 'Aryan', 'Vivaan',
    'Dhruv', 'Ishaan', 'Kabir', 'Lakshay', 'Arnav', 'Shreyas', 'Vedant'
]

FIRST_NAMES_FEMALE = [
    'Aadhya', 'Ananya', 'Diya', 'Ishita', 'Kavya', 'Meera', 'Navya', 'Priya',
    'Riya', 'Sara', 'Tara', 'Zara', 'Anika', 'Kiara', 'Saanvi'
]

LAST_NAMES = [
    'Sharma', 'Patel', 'Kumar', 'Singh', 'Gupta', 'Reddy', 'Agarwal', 'Joshi',
    'Verma', 'Mehta', 'Desai', 'Kapoor', 'Nair', 'Rao', 'Iyer', 'Malhotra',
    'Khanna', 'Bose', 'Das', 'Sinha', 'Trivedi', 'Pandey', 'Saxena', 'Mishra'
]

# Email domains
EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'student.edu']

# Address templates
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
AREAS = ['Sector', 'Block', 'Street', 'Avenue', 'Road', 'Colony', 'Nagar', 'Park']


def generate_phone_number():
    """Generate realistic 10-digit phone number."""
    return f"{random.randint(7, 9)}{random.randint(100000000, 999999999)}"


def generate_email(first_name, last_name):
    """Generate email address."""
    username = f"{first_name.lower()}.{last_name.lower()}"
    domain = random.choice(EMAIL_DOMAINS)
    return f"{username}@{domain}"


def generate_address():
    """Generate realistic address."""
    number = random.randint(1, 999)
    area_type = random.choice(AREAS)
    area_num = random.randint(1, 50)
    city = random.choice(CITIES)
    pincode = random.randint(100000, 999999)
    return f"{number}, {area_type} {area_num}, {city} - {pincode}"


def generate_student_profile(index, existing_names):
    """Generate a complete student profile."""
    # Determine gender
    gender = random.choice(GENDERS)
    
    # Generate name ensuring uniqueness
    while True:
        if gender == 'Male':
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)
        
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        
        if full_name not in existing_names:
            existing_names.add(full_name)
            break
    
    # Generate other details
    grade = random.choice(GRADES)
    section = random.choice(SECTIONS)
    age = 14 + int(grade)  # Realistic age based on grade
    email = generate_email(first_name, last_name)
    phone = generate_phone_number()
    address = generate_address()
    
    return {
        'name': full_name,
        'grade': grade,
        'section': section,
        'age': age,
        'gender': gender,
        'email': email,
        'phone': phone,
        'address': address
    }


def generate_score(base_performance='average', subject_strength=None):
    """
    Generate realistic exam scores.
    
    Args:
        base_performance: 'excellent', 'good', 'average', 'below_average'
        subject_strength: If True, student is strong in this subject
    """
    # Base score ranges
    ranges = {
        'excellent': (85, 98),
        'good': (70, 90),
        'average': (55, 75),
        'below_average': (40, 60)
    }
    
    min_score, max_score = ranges[base_performance]
    
    # Adjust for subject strength
    if subject_strength:
        min_score += 10
        max_score = min(98, max_score + 10)
    
    # Generate score with some randomness
    score = random.randint(min_score, max_score)
    
    # Add slight variation (±3 points)
    score += random.randint(-3, 3)
    
    # Ensure score is within 0-100
    return max(0, min(100, score))


def generate_exam_date(exam_type, base_date=None):
    """Generate realistic exam dates."""
    if base_date is None:
        base_date = datetime.now()
    
    # Different exam types at different times
    exam_offsets = {
        'Quiz 1': -120,      # 4 months ago
        'Quiz 2': -90,       # 3 months ago
        'Unit Test 1': -75,  # 2.5 months ago
        'Midterm': -60,      # 2 months ago
        'Unit Test 2': -30,  # 1 month ago
        'Final': -15         # 2 weeks ago
    }
    
    days_offset = exam_offsets.get(exam_type, -30)
    # Add some randomness (±5 days)
    days_offset += random.randint(-5, 5)
    
    exam_date = base_date + timedelta(days=days_offset)
    return exam_date.strftime('%Y-%m-%d')


def add_mock_data():
    """Main function to add comprehensive mock data."""
    print("=" * 70)
    print("ScoreSense Mock Data Generator")
    print("=" * 70)
    print()
    
    # Check if data already exists
    existing_students = get_all_students()
    if existing_students:
        print(f"⚠️  Database already contains {len(existing_students)} student(s).")
        response = input("Do you want to add more students? (y/n): ").lower()
        if response != 'y':
            print("Cancelled.")
            return
    
    print(f"\nGenerating {NUM_STUDENTS} students with comprehensive exam data...")
    print()
    
    existing_names = set(s['name'] for s in existing_students)
    students_added = 0
    exams_added = 0
    
    # Assign performance levels (realistic distribution)
    performance_distribution = (
        ['excellent'] * 3 +      # Top 10%
        ['good'] * 10 +          # 33%
        ['average'] * 14 +       # 47%
        ['below_average'] * 3    # 10%
    )
    random.shuffle(performance_distribution)
    
    for i in range(NUM_STUDENTS):
        try:
            # Generate student profile
            student = generate_student_profile(i + 1, existing_names)
            
            # Add student to database
            student_id = add_student(
                name=student['name'],
                grade=student['grade'],
                section=student['section'],
                age=student['age'],
                gender=student['gender'],
                email=student['email'],
                phone=student['phone'],
                address=student['address']
            )
            
            if not student_id:
                print(f"❌ Failed to add student: {student['name']} (duplicate)")
                continue
            
            students_added += 1
            
            # Get student's base performance level
            base_performance = performance_distribution[i % len(performance_distribution)]
            
            # Randomly assign 2-3 strong subjects per student
            strong_subjects = random.sample(SUBJECTS, k=random.randint(2, 3))
            
            # Generate exams for this student
            num_subjects = random.randint(5, 8)  # Each student takes 5-8 subjects
            student_subjects = random.sample(SUBJECTS, k=num_subjects)
            
            print(f"✅ Added: {student['name']} (Grade {student['grade']}{student['section']}, {base_performance} performer)")
            
            # Add multiple exams
            for exam_name in EXAMS:
                scores = {}
                
                for subject in student_subjects:
                    # Check if this is a strong subject for the student
                    is_strong = subject in strong_subjects
                    score = generate_score(base_performance, is_strong)
                    scores[subject] = score
                
                # Add exam with all subject scores
                exam_date = generate_exam_date(exam_name)
                success = add_complete_exam(
                    student_id=student_id,
                    exam_name=exam_name,
                    marks_dict=scores
                )
                
                if success:
                    exams_added += 1
                    avg_score = sum(scores.values()) / len(scores)
                    print(f"   📝 {exam_name}: {len(scores)} subjects, avg: {avg_score:.1f}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error adding student {i+1}: {e}")
            continue
    
    print("=" * 70)
    print("✨ Mock Data Generation Complete!")
    print("=" * 70)
    print(f"Students added: {students_added}")
    print(f"Exams added: {exams_added}")
    print(f"Total exam scores: {exams_added * 6} (approximately)")
    print()
    print("Summary:")
    print(f"  - {NUM_STUDENTS} students across grades {', '.join(GRADES)}")
    print(f"  - {len(SUBJECTS)} subjects: {', '.join(SUBJECTS[:4])}...")
    print(f"  - {len(EXAMS)} exam types per student")
    print(f"  - Realistic performance distribution (excellent to below average)")
    print(f"  - Complete profiles with contact info and addresses")
    print()
    print("🎓 You can now:")
    print("   - View student list at http://localhost:5000/students")
    print("   - Check statistics at http://localhost:5000/stats")
    print("   - View individual student details")
    print("   - Test graphs and predictions")
    print()


if __name__ == '__main__':
    try:
        add_mock_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
