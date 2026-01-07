# ScoreSense - AI-Powered Student Management System

A comprehensive Flask web application for managing student scores with natural language processing, statistics, visualizations, and AI-powered predictions.

## Features

### ✅ Core Features
- **Student Profile Management**: Comprehensive student profiles with personal details (grade, section, age, gender, contact info)
- **Multi-Exam Support**: Track unlimited exams per student with organized exam history
- **Natural Language Commands**: Control the system using plain English
- **Advanced Statistics**: Class averages, toppers, subject difficulty rankings, detailed student analytics
- **Data Visualizations**: Beautiful graphs using Matplotlib with multiple chart types
- **AI Predictions**: Linear regression-based score predictions
- **Material Design 3**: Modern UI with glass morphism and smooth animations
- **SQLite Database**: Persistent storage with comprehensive exam history tracking

### 🤖 Natural Language Commands
Execute actions using natural language:
- "Add student Krish in grade 10 section A"
- "Add complete exam for Krish: Midterm with math 95, physics 80, chemistry 88"
- "Show class topper"
- "Predict Sneha's next math score"
- "Compare scores of the class in chemistry"
- "Update John's profile with new email"
- "Delete Sarah"

### 📊 Visualizations
- Student performance bar charts
- Subject average comparisons
- Score distribution histograms
- Class-wide comparison charts
- Trend analysis graphs

### 📈 Statistics & Analytics
- Overall class average
- Subject-wise averages
- Class topper identification
- Subject difficulty ranking
- Score distribution analysis
- Student ranking system

### 🔮 AI Predictions
- Linear regression model for score prediction
- Confidence levels (high/medium/low)
- Trend analysis (improving/declining)
- Historical data tracking
- Batch predictions for entire class

## Project Structure

```
score_analyser/
│
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates
│   ├── index.html             # Dashboard
│   ├── add_student.html       # Add student profile (no exams)
│   ├── student_list.html      # Students listing
│   ├── edit_student.html      # Edit profile & manage exams
│   ├── student_detail.html    # Detailed student analytics
│   ├── stats.html             # Statistics page
│   └── command.html           # NL command interface
│
├── static/                     # Static assets
│   ├── styles.css             # Main stylesheet
│   └── script.js              # Frontend JavaScript
│
├── core/                       # Core modules
│   ├── nlu.py                 # Natural language understanding
│   ├── stats.py               # Statistics calculations
│   ├── graphs.py              # Graph generation
│   └── predict.py             # Prediction models
│
├── models/                     # Database models
│   └── student_model.py       # Student CRUD operations
│
└── db/                         # Database storage
    └── students.db            # SQLite database (auto-created)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- matplotlib 3.8.2
- numpy 1.26.2
- scikit-learn 1.3.2

### Step 2: Run the Application

```powershell
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Adding Students
1. Navigate to "Add Student" page
2. Enter student profile information:
   - Name (required)
   - Grade, Section, Age
   - Gender
   - Email, Phone, Address
3. Click "Add Student"
4. Navigate to "Edit Student" to add exams
5. Use "Add New Complete Exam" section to add all subjects for an exam at once

**OR** use natural language:
```
Command: "Add student John in grade 11 section B"
Command: "Add complete exam for John: Finals with math 90, physics 85, chemistry 92"
```

### Viewing Statistics
- Click "Statistics" in navigation
- View class averages, toppers, difficulty rankings
- Generate graphs for visual analysis

### Making Predictions
Use the command interface:
```
Command: "Predict Sarah's math score"
```

The system will:
- Analyze historical data
- Use linear regression model
- Provide prediction with confidence level
- Show trend analysis

### Comparing Performance
```
Command: "Compare scores in chemistry"
```

Displays ranked list of all students in that subject.

## API Endpoints

### Web Routes
- `GET /` - Dashboard
- `GET /students` - List all students
- `GET /add` - Add student profile form
- `POST /add` - Create student profile
- `GET /edit/<id>` - Edit student form
- `POST /edit/<id>` - Update student profile
- `POST /student/<id>/add_complete_exam` - Add complete exam with all subjects
- `GET /student/<id>/stats` - Detailed student analytics page
- `POST /delete/<id>` - Delete student
- `GET /stats` - Statistics page
- `GET /command` - Command interface
- `POST /command` - Execute NL command
- `GET /graph/<type>` - Generate graph

### REST API
- `GET /api/students` - Get all students (JSON)
- `GET /api/stats` - Get statistics (JSON)
- `GET /predict/<name>/<subject>` - Get prediction (JSON)

## Technical Details

### NLU Parser
Uses regex-based heuristic parsing to extract:
- **Intent**: ADD_STUDENT, UPDATE_STUDENT, DELETE_STUDENT, SHOW_TOPPER, PREDICT, etc.
- **Entities**: Student names, subjects, scores
- **Context**: Subject-specific or overall queries

### Prediction Model
- Uses scikit-learn's LinearRegression
- Requires minimum 2 historical data points
- Calculates R² score for confidence
- Falls back to heuristic for limited data

### Database Schema

**students table:**
- id (PRIMARY KEY)
- name (TEXT, UNIQUE)
- marks (TEXT, JSON - legacy field)
- grade (TEXT)
- section (TEXT)
- age (INTEGER)
- gender (TEXT)
- email (TEXT)
- phone (TEXT)
- address (TEXT)
- created_at (TIMESTAMP)

**exams table:**
- id (PRIMARY KEY)
- student_id (INTEGER, FOREIGN KEY)
- exam_name (TEXT) - Groups subjects by exam
- subject (TEXT)
- score (REAL)
- exam_date (TIMESTAMP)

## Example Workflow

1. **Add Student Profiles**
   - Add Alice (Grade 10, Section A, age 15, alice@school.com)
   - Add Bob (Grade 10, Section B, age 16, bob@school.com)
   - Add Carol (Grade 10, Section A, age 15, carol@school.com)

2. **Add Exams for Each Student**
   - Alice - Midterm Exam: Math 92, Physics 88, Chemistry 85
   - Bob - Midterm Exam: Math 78, Physics 82, Chemistry 90
   - Carol - Midterm Exam: Math 95, Physics 91, Chemistry 87

3. **View Detailed Student Stats**
   - Navigate to student detail page
   - View profile information
   - See exam history in accordion layout
   - Analyze subject-wise performance trends
   - Generate charts (bar, line, pie, radar)

4. **View Class Statistics**
   - Class average: ~87.5
   - Topper: Carol (91.0)
   - Hardest subject: Physics (87.0)

5. **Make Predictions**
   ```
   Predict Alice's next math score
   → Predicted: 93.5 (High confidence, Improving trend)
   ```

6. **Compare Performance**
   ```
   Compare scores in chemistry
   → 1. Bob (90), 2. Carol (87), 3. Alice (85)
   ```

## Customization

### Adding New Subjects
Simply add students with new subjects - the system automatically detects and tracks them.

### Modifying Prediction Algorithm
Edit `core/predict.py` to customize:
- Change from LinearRegression to other models
- Adjust confidence thresholds
- Modify heuristic fallback logic

### Styling
Edit `static/styles_m3.css` to customize:
- Material Design 3 color scheme
- Glass morphism effects
- Animation timing and easing
- Layout and responsive breakpoints
- Accordion styles

## Troubleshooting

### Database Not Created
- Ensure write permissions in the `db/` directory
- Database is auto-created on first run

### Graphs Not Displaying
- Ensure matplotlib is installed correctly
- Check browser console for JavaScript errors

### Prediction Errors
- Requires at least one historical score
- Multiple exams improve accuracy

## Future Enhancements

Potential improvements:
- Export data to CSV/Excel
- Email reports
- Multi-class support
- Teacher authentication
- Mobile app
- Advanced ML models (Random Forest, Neural Networks)
- Real-time collaboration
- Parent portal

## License

MIT License - Free to use and modify

## Author

Created with ❤️ using Flask, Python, and AI

---

**Enjoy managing student scores with AI! 🎓📊🤖**
