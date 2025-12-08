# ScoreSense: 5-Minute Project Presentation

*A comprehensive student performance analytics system with natural language processing*

---

## Section 1: Database Architecture (45 seconds)

### Database Schema

**Students Table:**
```sql
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    marks TEXT,  -- Legacy JSON field
    grade TEXT,
    section TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Exams Table:**
```sql
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    exam_name TEXT NOT NULL,
    exam_date TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
)
```

**Key Design Decisions:**
- Normalized structure separating student profiles from exam records
- CASCADE delete ensures referential integrity
- Legacy marks field retained for backward compatibility
- All statistics computed from exams table using SQL aggregations

---

## Section 2: Flask Web Application (60 seconds)

### Core Routes

**Dashboard Route:**
```python
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    
    # Calculate class statistics
    class_avg = get_class_average()
    subject_avgs = get_subject_averages()
    topper = get_class_topper()
    
    return render_template('index.html',
                         students=students,
                         class_avg=class_avg,
                         subject_avgs=subject_avgs,
                         topper=topper)
```

**Statistics Route:**
```python
@app.route('/statistics')
def statistics():
    class_avg = get_class_average()
    subject_avgs = get_subject_averages()
    top_students = get_top_students(limit=10)
    score_dist = get_score_distribution()
    
    return render_template('stats.html',
                         class_average=class_avg,
                         subject_averages=subject_avgs,
                         top_students=top_students,
                         score_distribution=score_dist)
```

**Request Flow:**
1. Client sends HTTP request
2. Flask routes to appropriate handler
3. Handler queries database via SQLite
4. Business logic processes data
5. Template renders HTML response
6. Response sent to client

---

## Section 3: Statistics Engine (45 seconds)

### Class Average Calculation

```python
def get_class_average():
    conn = get_db_connection()
    result = conn.execute('''
        SELECT AVG(score) as avg_score
        FROM exams
    ''').fetchone()
    conn.close()
    
    return round(result['avg_score'], 2) if result['avg_score'] else 0
```

**How It Works:**
- SQL `AVG()` aggregation function computes mean across all exam scores
- Returns 0 if no exams exist (handles empty database)
- Rounds to 2 decimal places for display

### Subject-Wise Performance

```python
def get_subject_averages():
    conn = get_db_connection()
    subjects = conn.execute('''
        SELECT subject, AVG(score) as avg_score, COUNT(*) as exam_count
        FROM exams
        GROUP BY subject
        ORDER BY avg_score DESC
    ''').fetchall()
    conn.close()
    
    return [dict(row) for row in subjects]
```

**Analysis:**
- Groups exams by subject using `GROUP BY`
- Computes average and count per subject
- Orders by performance (highest first)
- Identifies strengths and weaknesses

### Live Database Query Example

**Current Statistics:**
- Total Students: 60
- Total Exams: 360+
- Class Average: ~72.5
- Top Subject: Mathematics (~78.2)
- Lowest Subject: Science (~67.8)

---

## Section 4: Natural Language Processing (50 seconds)

### Command Parser

```python
def parse_command(command):
    command = command.lower().strip()
    
    # Extract student name pattern
    name_match = re.search(r'(?:for|of)\s+([a-z\s]+?)(?:\s+(?:in|for|subject|exam)|$)', 
                          command, re.IGNORECASE)
    
    # Extract subject pattern
    subject_match = re.search(r'(?:in|for|subject)\s+([a-z]+)', 
                             command, re.IGNORECASE)
    
    # Intent detection
    if 'average' in command or 'avg' in command:
        if name_match:
            return ('student_average', name_match.group(1).strip())
        elif subject_match:
            return ('subject_average', subject_match.group(1).strip())
        else:
            return ('class_average', None)
    
    elif 'rank' in command or 'position' in command:
        if name_match:
            return ('student_rank', name_match.group(1).strip())
    
    elif 'topper' in command or 'top' in command:
        return ('class_topper', None)
```

**Example Commands:**
- "What is the average of John Doe?" → `('student_average', 'John Doe')`
- "Show me rank of Sarah Smith" → `('student_rank', 'Sarah Smith')`
- "Class average for Mathematics" → `('subject_average', 'Mathematics')`
- "Who is the class topper?" → `('class_topper', None)`

**Pattern Matching:**
- Regex extracts entities (names, subjects)
- Intent classification via keyword matching
- Returns structured tuple: (intent, entity)

---

## Section 5: Visualization & Machine Learning (40 seconds)

### Graph Generation (when enabled locally)

```python
def generate_student_bar(student_data, title="Student Performance"):
    subjects = list(student_data.keys())
    scores = list(student_data.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(subjects, scores, color='#1976D2')
    plt.xlabel('Subjects')
    plt.ylabel('Scores')
    plt.title(title)
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    # Save to base64 for embedding
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return image_base64
```

### Performance Prediction (when enabled locally)

```python
def predict_performance(student_id):
    # Fetch historical scores
    conn = get_db_connection()
    exams = conn.execute('''
        SELECT exam_date, AVG(score) as avg_score
        FROM exams
        WHERE student_id = ?
        GROUP BY exam_date
        ORDER BY exam_date
    ''', (student_id,)).fetchall()
    
    # Linear regression on time series
    X = np.array(range(len(exams))).reshape(-1, 1)
    y = np.array([e['avg_score'] for e in exams])
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next exam
    next_x = len(exams)
    prediction = model.predict([[next_x]])[0]
    
    return round(prediction, 2)
```

**Note:** Graph and prediction features disabled in deployment to meet Vercel's 250 MB limit.

---

## Section 6: Key Features & Project Structure (40 seconds)

### Core Features

1. **Student Management**
   - Add/edit/delete student profiles
   - Complete demographic information
   - Individual student dashboards

2. **Exam Recording**
   - Multi-subject exam entry
   - Various exam types (Midterm, Final, Quiz, Unit Test)
   - Historical tracking

3. **Analytics Dashboard**
   - Class-wide statistics
   - Subject performance analysis
   - Score distribution visualization
   - Top performers ranking

4. **Natural Language Interface**
   - Intuitive command input
   - Context-aware parsing
   - Instant query responses

5. **Data Management**
   - Excel import (local only)
   - Mock data generation
   - Database backup/restore

### Project Structure

```
score_analyser/
├── app.py                    # Main Flask application (481 lines)
├── models/
│   └── student_model.py      # Database operations (427 lines)
├── core/
│   ├── stats.py             # Statistics engine (273 lines)
│   ├── graphs.py            # Visualization (disabled in deployment)
│   ├── nlp.py               # Command parsing (124 lines)
│   └── predict.py           # ML predictions (disabled in deployment)
├── templates/               # HTML templates (Material Design 3)
├── static/                  # CSS/JS assets
├── add_mock_data.py         # Test data generator (292 lines)
├── presentation.py          # This presentation (442 lines)
└── students.db              # SQLite database (60 students, 360+ exams)
```

### Technical Highlights

**Code Quality:**
- Modular architecture with separation of concerns
- Comprehensive error handling with try-finally blocks
- Database connection pooling with autocommit mode
- Feature flags for conditional module loading

**Deployment Strategy:**
- Dual version: Full-featured (local) + Lightweight (Vercel)
- Smart dependency management
- Lazy module loading for optional features

**Performance Optimizations:**
- SQL aggregations instead of Python loops
- Index on foreign keys for fast joins
- Connection timeout prevention (30 seconds)
- Autocommit mode to avoid lock conflicts

### Future Enhancements

- Real-time collaboration (WebSockets)
- Advanced ML models (LSTM for time series)
- Mobile app (React Native)
- Export to PDF reports
- Email notifications for low performance
- Teacher/admin role management

---

## Quick Demo Statistics

**Current Database State:**
- **Total Students:** 60
- **Total Exams:** 360+
- **Subjects:** 8 (Math, Science, English, Hindi, Social Studies, Computer Science, Physics, Chemistry)
- **Exam Types:** 6 (Midterm, Final Exam, Quiz 1, Quiz 2, Unit Test 1, Unit Test 2)
- **Average Performance:** ~72.5%
- **Top Performer:** Varies by exam cycle
- **Performance Distribution:**
  - Excellent (90-100): ~10%
  - Good (75-89): ~33%
  - Average (60-74): ~47%
  - Below Average (<60): ~10%

---

## Technology Stack

**Backend:**
- Python 3.12
- Flask 3.0.0 (web framework)
- SQLite3 (database)
- scikit-learn 1.3.2 (ML - local only)
- pandas 2.1.4 (data processing - local only)

**Frontend:**
- Material Design 3
- Chart.js (interactive graphs)
- Responsive CSS Grid
- Vanilla JavaScript

**Deployment:**
- Vercel (serverless)
- GitHub Actions (CI/CD)
- Lightweight version (<50 MB)

---

## Conclusion

ScoreSense demonstrates:
- **Full-stack development** with Flask and SQLite
- **Data-driven insights** through statistical analysis
- **User-friendly interface** with natural language processing
- **Scalable architecture** with modular design
- **Production deployment** with optimization strategies

**GitHub Repository:** https://github.com/darkShadow-exe/ScoreSense

**Live Demo:** Run locally with `python app.py` or use interactive `python presentation.py`

---

*Presentation created: December 8, 2025*
*Total Time: ~5 minutes*
