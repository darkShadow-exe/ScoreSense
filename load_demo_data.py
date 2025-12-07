"""
Demo Data Loader
Run this script to populate the database with sample students for testing.
"""

from models.student_model import add_student

def load_demo_data():
    """Load sample students into the database."""
    
    demo_students = [
        {
            'name': 'Alice',
            'marks': {
                'math': 92,
                'physics': 88,
                'chemistry': 85,
                'biology': 90
            }
        },
        {
            'name': 'Bob',
            'marks': {
                'math': 78,
                'physics': 82,
                'chemistry': 90,
                'biology': 76
            }
        },
        {
            'name': 'Carol',
            'marks': {
                'math': 95,
                'physics': 91,
                'chemistry': 87,
                'biology': 93
            }
        },
        {
            'name': 'David',
            'marks': {
                'math': 68,
                'physics': 72,
                'chemistry': 75,
                'biology': 70
            }
        },
        {
            'name': 'Emma',
            'marks': {
                'math': 88,
                'physics': 85,
                'chemistry': 92,
                'biology': 89
            }
        },
        {
            'name': 'Frank',
            'marks': {
                'math': 82,
                'physics': 79,
                'chemistry': 81,
                'biology': 84
            }
        },
        {
            'name': 'Grace',
            'marks': {
                'math': 97,
                'physics': 94,
                'chemistry': 96,
                'biology': 95
            }
        },
        {
            'name': 'Henry',
            'marks': {
                'math': 73,
                'physics': 76,
                'chemistry': 78,
                'biology': 72
            }
        },
    ]
    
    print("Loading demo data...")
    
    for student in demo_students:
        result = add_student(student['name'], student['marks'])
        if result:
            print(f"✓ Added {student['name']}")
        else:
            print(f"✗ {student['name']} already exists")
    
    print("\nDemo data loaded successfully!")
    print("\nYou can now:")
    print("1. View students at http://localhost:5000/students")
    print("2. See statistics at http://localhost:5000/stats")
    print("3. Try commands at http://localhost:5000/command")
    print("\nExample commands:")
    print('  - "Show class topper"')
    print('  - "Predict Grace\'s math score"')
    print('  - "Compare scores in physics"')

if __name__ == '__main__':
    load_demo_data()
