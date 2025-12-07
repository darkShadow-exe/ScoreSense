# Testing Guide - Score Analyser

## Manual Testing Checklist

### 1️⃣ Installation Test
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] No errors during installation
- [ ] All packages installed successfully

### 2️⃣ Application Startup
- [ ] Run `python app.py`
- [ ] Server starts without errors
- [ ] Database created in `db/students.db`
- [ ] Access http://localhost:5000

### 3️⃣ Dashboard Page (/)
- [ ] Page loads successfully
- [ ] Shows "0 Total Students" initially
- [ ] All navigation links work
- [ ] Action cards are clickable
- [ ] Quick commands section visible

### 4️⃣ Add Student Functionality (/add)
**Test 1: Basic Addition**
- [ ] Navigate to Add Student page
- [ ] Enter name: "TestStudent1"
- [ ] Add Math: 85
- [ ] Add Physics: 90
- [ ] Click "Add Student"
- [ ] Success message displayed
- [ ] Redirected to students list
- [ ] Student appears in list

**Test 2: Multiple Subjects**
- [ ] Add "TestStudent2"
- [ ] Add 4+ subjects
- [ ] Click "Add Another Subject" button works
- [ ] All subjects saved correctly

**Test 3: Validation**
- [ ] Try submitting without name → Error
- [ ] Try submitting without scores → Error
- [ ] Try duplicate name → "Student already exists"

### 5️⃣ Students List (/students)
- [ ] All students displayed in table
- [ ] Scores shown correctly
- [ ] Average calculated properly
- [ ] Edit button works
- [ ] Delete button works (with confirmation)
- [ ] Empty state shown when no students

### 6️⃣ Edit Student (/edit/<id>)
- [ ] Edit form pre-populated
- [ ] Can change name
- [ ] Can modify scores
- [ ] Can add new subjects
- [ ] Update saves correctly
- [ ] Redirects to student list

### 7️⃣ Delete Student
- [ ] Delete shows confirmation
- [ ] Canceling works
- [ ] Confirming deletes student
- [ ] Student removed from list
- [ ] Statistics updated

### 8️⃣ Statistics Page (/stats)
**After loading demo data:**
- [ ] Total students count correct
- [ ] Class average calculated
- [ ] Topper identified correctly
- [ ] Lowest scorer shown
- [ ] Subject averages displayed
- [ ] Progress bars animate
- [ ] Difficulty ranking shown
- [ ] Score distribution displayed

### 9️⃣ Natural Language Commands (/command)

**Test Commands:**

1. **Add Student**
   ```
   Add Sarah with 92 in math and 88 in physics
   ```
   - [ ] Student created
   - [ ] Marks saved correctly
   - [ ] Success message shown

2. **Show Topper**
   ```
   Show class topper
   ```
   - [ ] Correct topper displayed
   - [ ] Average shown
   - [ ] All marks listed

3. **Subject Topper**
   ```
   Show topper in math
   ```
   - [ ] Subject-specific topper shown
   - [ ] Score displayed

4. **Update Student**
   ```
   Update Sarah with 95 in chemistry
   ```
   - [ ] New subject added
   - [ ] Existing marks preserved
   - [ ] Success confirmation

5. **Delete Student**
   ```
   Delete Sarah
   ```
   - [ ] Student removed
   - [ ] Success message

6. **Predict Score**
   ```
   Predict Alice's math score
   ```
   - [ ] Prediction shown
   - [ ] Confidence level displayed
   - [ ] Method explained
   - [ ] Trend indicated

7. **Compare Scores**
   ```
   Compare scores in physics
   ```
   - [ ] All students listed
   - [ ] Ranked by score
   - [ ] Average shown
   - [ ] Table formatted correctly

8. **Show Statistics**
   ```
   Show class average
   ```
   - [ ] Statistics displayed
   - [ ] All metrics shown

9. **Invalid Command**
   ```
   xyz random text
   ```
   - [ ] Error message shown
   - [ ] Helpful suggestions given

### 🔟 Graph Generation

**Test Graphs:**
1. **Student Bar Chart**
   - [ ] Load graph for specific student
   - [ ] All subjects shown
   - [ ] Scores correct
   - [ ] Labels visible

2. **Subject Average Bar**
   - [ ] All subjects displayed
   - [ ] Averages calculated correctly
   - [ ] Values labeled

3. **Distribution Histogram**
   - [ ] Score ranges shown
   - [ ] Counts correct
   - [ ] Visual clear

4. **Comparison Chart**
   - [ ] Select a subject
   - [ ] All students shown
   - [ ] Ranked correctly
   - [ ] Readable labels

5. **Student Comparison**
   - [ ] All students compared
   - [ ] Multiple subjects shown
   - [ ] Legend clear
   - [ ] Colors distinct

### 1️⃣1️⃣ Prediction System

**Setup:**
1. Add student with initial scores
2. Update student 2-3 times with new scores
3. Run prediction

**Tests:**
- [ ] Prediction uses linear regression
- [ ] Confidence level appropriate
- [ ] Trend direction correct
- [ ] R² score shown
- [ ] Message explanatory

**Edge Cases:**
- [ ] Prediction with 1 data point (heuristic)
- [ ] Prediction with no history (baseline)
- [ ] Prediction for non-existent student (error)
- [ ] Prediction for non-existent subject (error)

### 1️⃣2️⃣ Responsive Design
- [ ] Test on mobile viewport (< 768px)
- [ ] Navigation collapses properly
- [ ] Tables scroll horizontally
- [ ] Cards stack vertically
- [ ] Forms remain usable
- [ ] Buttons accessible

### 1️⃣3️⃣ Data Persistence
- [ ] Stop server
- [ ] Restart server
- [ ] Data still present
- [ ] History preserved
- [ ] No data loss

### 1️⃣4️⃣ Error Handling
- [ ] Invalid student ID → Redirects
- [ ] Missing parameters → Error message
- [ ] Database errors → Graceful failure
- [ ] Graph generation failure → Error shown

### 1️⃣5️⃣ API Endpoints

**GET /api/students**
- [ ] Returns JSON
- [ ] All students included
- [ ] Marks formatted correctly

**GET /api/stats**
- [ ] Returns statistics JSON
- [ ] All metrics included
- [ ] Format correct

**GET /predict/<name>/<subject>**
- [ ] Returns prediction JSON
- [ ] Error handling works
- [ ] Valid predictions accurate

---

## Automated Test Script

Run this in Python to test core functions:

```python
# test_core.py
from models.student_model import add_student, get_all_students, delete_student
from core.nlu import parse_command
from core.stats import get_all_stats
from core.predict import predict_score

# Test 1: Add student
print("Test 1: Adding student...")
result = add_student("TestUser", {"math": 90, "physics": 85})
assert result is not None, "Failed to add student"
print("✓ Passed")

# Test 2: Retrieve students
print("Test 2: Retrieving students...")
students = get_all_students()
assert len(students) > 0, "No students found"
print(f"✓ Passed - Found {len(students)} students")

# Test 3: NLU parsing
print("Test 3: Parsing command...")
parsed = parse_command("Add John with 95 in math")
assert parsed['intent'] == 'ADD_STUDENT', "Wrong intent"
assert parsed['name'] == 'John', "Wrong name"
assert parsed['marks']['math'] == 95, "Wrong score"
print("✓ Passed")

# Test 4: Statistics
print("Test 4: Calculating statistics...")
stats = get_all_stats()
assert stats['total_students'] > 0, "No students in stats"
assert stats['class_average'] > 0, "Invalid average"
print("✓ Passed")

# Cleanup
print("\nCleaning up test data...")
student = get_student_by_name("TestUser")
if student:
    delete_student(student['id'])
print("✓ Cleanup complete")

print("\n✅ All tests passed!")
```

---

## Performance Testing

### Load Testing
1. Add 100+ students
2. Check page load times
3. Graph generation speed
4. Query performance

### Stress Testing
1. Rapid command execution
2. Concurrent graph requests
3. Large dataset statistics
4. Multiple predictions

---

## Bug Reporting Template

```
**Bug Title:** 
**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**

**Actual Behavior:**

**Screenshots:**

**Environment:**
- OS: 
- Browser: 
- Python Version: 

**Additional Context:**
```

---

## Test Results Log

| Test | Date | Result | Notes |
|------|------|--------|-------|
| Installation | | ⬜ | |
| Dashboard | | ⬜ | |
| Add Student | | ⬜ | |
| Edit Student | | ⬜ | |
| Delete Student | | ⬜ | |
| Statistics | | ⬜ | |
| Commands | | ⬜ | |
| Graphs | | ⬜ | |
| Predictions | | ⬜ | |
| API | | ⬜ | |

Legend: ⬜ Not Tested | ✅ Passed | ❌ Failed | ⚠️ Partial

---

**Test thoroughly before production use! 🧪✅**
