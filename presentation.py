"""
ScoreSense - 5 Minute Project Presentation Script
A comprehensive student performance tracking system with AI-powered insights

This script provides a complete walkthrough of the project features and code.
Time: ~5 minutes | Sections: 6 | Format: Interactive demonstration
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.student_model import get_all_students, get_student_by_name
from core.stats import get_all_stats, get_class_topper, get_subject_averages


def print_section(title, number):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"SECTION {number}: {title}")
    print("=" * 80)


def print_code(description, code):
    """Print code snippet with description."""
    print(f"\n📌 {description}")
    print("\n```python")
    print(code)
    print("```")


def pause(message="Press Enter to continue..."):
    """Pause for dramatic effect."""
    input(f"\n{message}")


def presentation():
    """Main presentation function."""
    
    # Introduction
    print("\n" * 2)
    print("=" * 80)
    print("                        SCORESENSE PROJECT PRESENTATION")
    print("                   Student Performance Tracking & Analytics")
    print("=" * 80)
    print("\n👨‍🎓 Project Overview:")
    print("   • Web-based student management system")
    print("   • Real-time analytics and visualizations")
    print("   • Natural language command interface")
    print("   • AI-powered score predictions")
    print("   • Excel import/export capabilities")
    print("\n🛠️  Tech Stack:")
    print("   • Backend: Flask (Python web framework)")
    print("   • Database: SQLite (lightweight, serverless)")
    print("   • ML: scikit-learn (predictions)")
    print("   • Visualization: matplotlib (charts)")
    print("   • Data Processing: pandas (Excel handling)")
    
    pause()
    
    # ============================================================================
    # SECTION 1: Database Architecture (45 seconds)
    # ============================================================================
    print_section("DATABASE ARCHITECTURE", 1)
    
    print("\n📊 Two-Table Design for Scalability:\n")
    
    print("TABLE 1: students")
    print("└─ Stores student profiles (name, grade, section, age, gender, contact info)")
    print_code(
        "Student table structure",
        """CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    grade TEXT,
    section TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""
    )
    
    print("\n\nTABLE 2: exams")
    print("└─ Stores all exam scores (one row per subject per exam)")
    print_code(
        "Exams table structure",
        """CREATE TABLE exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT NOT NULL,
    score REAL NOT NULL,
    exam_name TEXT NOT NULL,
    exam_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
)"""
    )
    
    print("\n✨ Why This Design?")
    print("   • Normalized: Prevents data duplication")
    print("   • Scalable: Easy to add unlimited exams")
    print("   • Flexible: Each exam can have different subjects")
    print("   • Efficient: Fast queries with proper indexing")
    
    pause()
    
    # ============================================================================
    # SECTION 2: Flask Web Application (60 seconds)
    # ============================================================================
    print_section("FLASK WEB APPLICATION", 2)
    
    print("\n🌐 Core Application Structure:\n")
    
    print_code(
        "Main Flask app setup",
        """from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    '''Dashboard - shows class statistics'''
    stats = get_all_stats()
    return render_template('index.html', stats=stats)

@app.route('/students')
def students():
    '''Student list with averages'''
    all_students = get_all_students()
    return render_template('student_list.html', students=all_students)"""
    )
    
    print("\n📍 Key Routes:")
    print("   • /              → Dashboard (statistics overview)")
    print("   • /students      → Student list with scores")
    print("   • /stats         → Detailed analytics page")
    print("   • /add           → Add new student")
    print("   • /command       → Natural language interface")
    print("   • /graph/<type>  → Dynamic chart generation")
    print("   • /import        → Excel file upload")
    
    print("\n💡 How Flask Works:")
    print("   1. Browser sends request to URL (e.g., /students)")
    print("   2. Flask finds matching @app.route decorator")
    print("   3. Executes function, gets data from database")
    print("   4. Renders HTML template with data")
    print("   5. Returns HTML to browser")
    
    pause()
    
    # ============================================================================
    # SECTION 3: Statistics Engine (45 seconds)
    # ============================================================================
    print_section("STATISTICS ENGINE", 3)
    
    print("\n📈 Real-Time Analytics Calculations:\n")
    
    print_code(
        "Class average calculation",
        """def get_class_average():
    '''Calculate overall class average from all exam scores'''
    conn = get_connection()
    cursor = conn.cursor()
    
    # SQL aggregation - averages all scores in exams table
    cursor.execute('SELECT AVG(score) as avg_score FROM exams')
    result = cursor.fetchone()
    
    return round(result['avg_score'], 2) if result else 0"""
    )
    
    print_code(
        "Finding the top performer",
        """def get_class_topper():
    '''Get student with highest average across all exams'''
    cursor.execute('''
        SELECT s.name, AVG(e.score) as avg_score
        FROM students s
        JOIN exams e ON s.id = e.student_id
        GROUP BY s.id, s.name
        ORDER BY avg_score DESC
        LIMIT 1
    ''')
    return cursor.fetchone()"""
    )
    
    print("\n📊 Statistics Provided:")
    print("   • Class average (all subjects)")
    print("   • Subject-wise averages")
    print("   • Top performer & lowest scorer")
    print("   • Score distribution (0-40, 41-60, 61-80, 81-100)")
    print("   • Individual student rankings")
    
    # Show live statistics
    try:
        stats = get_all_stats()
        print("\n🔴 LIVE DATA FROM DATABASE:")
        print(f"   → Class Average: {stats.get('class_average', 0)}")
        topper = stats.get('topper')
        if topper:
            print(f"   → Class Topper: {topper.get('name', 'N/A')} ({topper.get('average', 0)})")
        print(f"   → Total Students: {stats.get('total_students', 0)}")
        print(f"   → Total Exams: {stats.get('total_exams', 0)}")
    except:
        print("\n   (Database not initialized)")
    
    pause()
    
    # ============================================================================
    # SECTION 4: Natural Language Processing (50 seconds)
    # ============================================================================
    print_section("NATURAL LANGUAGE INTERFACE", 4)
    
    print("\n💬 Users can type commands in plain English!\n")
    
    print_code(
        "Command parsing with regex",
        """import re

def parse_command(text):
    '''Extract intent and entities from natural language'''
    text = text.lower()
    
    # Intent detection
    if 'add' in text or 'create' in text:
        return parse_add_student(text)
    elif 'topper' in text or 'best' in text:
        return parse_show_topper(text)
    
def extract_name(text):
    '''Extract student name using regex patterns'''
    patterns = [
        r'(?:add|create)\\s+([A-Za-z\\s]+?)(?:\\s+in|\\s+with|$)',
        r'([A-Za-z\\s]+?)\\s+(?:in grade|with)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()"""
    )
    
    print("\n📝 Example Commands:")
    print("   → 'Add student John Smith in grade 10 section A'")
    print("   → 'Show topper in mathematics'")
    print("   → 'Add exam Midterm for Alice with math: 90, physics: 85'")
    print("   → 'Predict score for Bob in chemistry'")
    print("   → 'Delete student John'")
    
    print("\n🧠 How It Works:")
    print("   1. User types natural language command")
    print("   2. Text is normalized (lowercase, trimmed)")
    print("   3. Intent detection (add/delete/show/predict)")
    print("   4. Regex patterns extract entities (names, scores)")
    print("   5. Structured data passed to database functions")
    print("   6. Result shown to user")
    
    pause()
    
    # ============================================================================
    # SECTION 5: Visualization & ML (40 seconds)
    # ============================================================================
    print_section("VISUALIZATION & MACHINE LEARNING", 5)
    
    print("\n📊 Dynamic Chart Generation:\n")
    
    print_code(
        "Creating bar charts with matplotlib",
        """import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_student_bar(student_name):
    '''Generate bar chart for student's subject scores'''
    student = get_student_by_name(student_name)
    
    subjects = list(student['latest_scores'].keys())
    scores = list(student['latest_scores'].values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(subjects, scores, color='#4CAF50')
    plt.ylabel('Scores')
    plt.title(f"{student_name}'s Performance")
    
    # Convert plot to base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    img_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return img_data"""
    )
    
    print("\n📈 Available Chart Types:")
    print("   • Bar Chart: Subject-wise scores")
    print("   • Pie Chart: Score distribution")
    print("   • Line Chart: Performance trends")
    print("   • Radar Chart: 360° performance view")
    
    print("\n🤖 AI Prediction Engine:")
    print_code(
        "Linear regression for score prediction",
        """from sklearn.linear_model import LinearRegression
import numpy as np

def predict_score(student_name, subject):
    '''Predict future score using past performance'''
    # Get historical scores
    scores = get_student_subject_history(student_name, subject)
    
    if len(scores) < 2:
        return {'error': 'Not enough data'}
    
    # Prepare data: X = exam numbers, y = scores
    X = np.array([[i] for i in range(len(scores))])
    y = np.array(scores)
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next score
    next_exam = [[len(scores)]]
    prediction = model.predict(next_exam)[0]
    
    return {
        'predicted_score': round(prediction, 2),
        'confidence': model.score(X, y)  # R² score
    }"""
    )
    
    pause()
    
    # ============================================================================
    # SECTION 6: Key Features Demo (40 seconds)
    # ============================================================================
    print_section("KEY FEATURES SUMMARY", 6)
    
    print("\n✨ What Makes ScoreSense Special?\n")
    
    print("1️⃣  COMPREHENSIVE STUDENT PROFILES")
    print("   • Complete contact information")
    print("   • Grade and section tracking")
    print("   • Unlimited exam history")
    
    print("\n2️⃣  ADVANCED ANALYTICS")
    print("   • Real-time statistics calculation")
    print("   • Subject-wise performance analysis")
    print("   • Automatic ranking and comparison")
    
    print("\n3️⃣  INTERACTIVE VISUALIZATIONS")
    print("   • Dynamic charts (bar, pie, line, radar)")
    print("   • Color-coded performance indicators")
    print("   • Responsive Material Design 3 UI")
    
    print("\n4️⃣  INTELLIGENT FEATURES")
    print("   • Natural language command processing")
    print("   • AI-powered score predictions")
    print("   • Excel import/export")
    
    print("\n5️⃣  SCALABLE ARCHITECTURE")
    print("   • SQLite database (no server needed)")
    print("   • Autocommit mode (no locking issues)")
    print("   • Clean separation of concerns")
    
    print("\n📁 Project Structure:")
    print("""
    score_analyser/
    ├── app.py                 # Main Flask application
    ├── models/
    │   └── student_model.py   # Database operations (CRUD)
    ├── core/
    │   ├── stats.py           # Statistics calculations
    │   ├── graphs.py          # Chart generation
    │   ├── nlu.py             # Natural language processing
    │   ├── predict.py         # ML predictions
    │   └── excel_import.py    # Excel handling
    ├── templates/             # HTML templates (Jinja2)
    ├── static/                # CSS, JavaScript
    └── db/                    # SQLite database
    """)
    
    print("\n🎯 Code Quality:")
    print("   • Modular design (separation of concerns)")
    print("   • Try-finally blocks (proper resource cleanup)")
    print("   • SQL injection prevention (parameterized queries)")
    print("   • Error handling throughout")
    print("   • Comprehensive documentation")
    
    pause()
    
    # Conclusion
    print("\n" * 2)
    print("=" * 80)
    print("                              CONCLUSION")
    print("=" * 80)
    
    print("\n💡 Technical Highlights:")
    print("   • Full-stack Python web application")
    print("   • RESTful API design")
    print("   • Relational database with normalization")
    print("   • Machine learning integration")
    print("   • Responsive user interface")
    
    print("\n🚀 Future Enhancements:")
    print("   • User authentication & roles")
    print("   • Email notifications for low scores")
    print("   • Advanced ML models (neural networks)")
    print("   • Mobile app version")
    print("   • Cloud deployment (Vercel/Heroku)")
    
    print("\n📊 Current Status:")
    try:
        students = get_all_students()
        total_exams = sum(len(get_student_by_name(s['name']).get('exams', [])) for s in students[:5])
        print(f"   • {len(students)} students in database")
        print(f"   • {total_exams}+ exam records")
        print("   • Fully functional and tested")
    except:
        print("   • Ready for deployment")
    
    print("\n" + "=" * 80)
    print("                    THANK YOU FOR YOUR ATTENTION!")
    print("=" * 80)
    print("\n🔗 GitHub: https://github.com/darkShadow-exe/ScoreSense")
    print("📧 Questions? Feel free to ask!")
    print("\n")


if __name__ == '__main__':
    try:
        presentation()
    except KeyboardInterrupt:
        print("\n\n⚠️  Presentation interrupted.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
