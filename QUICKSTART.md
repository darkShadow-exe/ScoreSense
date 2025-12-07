# Quick Start Guide - Score Analyser

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
Open PowerShell in the project directory and run:
```powershell
pip install -r requirements.txt
```

### Step 2: Start the Application
```powershell
python app.py
```

You should see:
```
Starting Score Analyser Application...
Access the application at: http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Quick Demo

### Option A: Add Students Manually
1. Click "Add Student"
2. Fill in name and subjects
3. Click "Add Student"

### Option B: Load Demo Data
Run the demo data loader:
```powershell
python load_demo_data.py
```

This will add 8 sample students with scores.

---

## 💡 Try These Commands

Go to the "Commands" page and try:

1. **Add a student:**
   ```
   Add John with 90 in math and 85 in physics
   ```

2. **Show the topper:**
   ```
   Show class topper
   ```

3. **Predict a score:**
   ```
   Predict Alice's math score
   ```

4. **Compare performance:**
   ```
   Compare scores in chemistry
   ```

5. **Update a student:**
   ```
   Update Bob with 95 in biology
   ```

---

## 📊 Explore Features

### Dashboard
- View overall statistics
- Quick access to all features
- Class performance overview

### Students Page
- See all students in a table
- View individual scores
- Edit or delete students
- Generate comparison graphs

### Statistics Page
- Detailed class analytics
- Subject difficulty ranking
- Score distribution
- Visual charts

### Commands Page
- Natural language interface
- AI-powered command parsing
- Instant results
- Example commands provided

---

## 🔧 Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Module Not Found Error
Make sure you're in the project directory:
```powershell
cd c:\Users\krish\Downloads\score_analyser
```

### Database Permission Error
Ensure you have write permissions in the project folder.

---

## 🎓 Educational Use Cases

### For Teachers:
- Track student progress
- Identify struggling students
- Predict exam outcomes
- Generate performance reports

### For Students:
- View your performance
- Compare with class average
- See improvement trends
- Set target scores

### For Administrators:
- Analyze class statistics
- Subject difficulty assessment
- Performance distributions
- Data-driven decisions

---

## 📝 Sample Workflow

1. **Start Fresh**
   ```powershell
   python app.py
   ```

2. **Load Demo Data**
   ```powershell
   python load_demo_data.py
   ```

3. **View Dashboard** (http://localhost:5000)
   - See 8 students loaded
   - Class average displayed
   - Topper identified

4. **Try Commands**
   - "Show topper in math" → Grace (97)
   - "Predict Emma's physics score" → ~86.5
   - "Compare scores in biology" → Full ranking

5. **Add New Student**
   - Use form or command
   - Instant statistics update
   - Graphs refresh automatically

6. **Make Predictions**
   - Requires multiple exam entries
   - Update student to add more data
   - Prediction accuracy improves

---

## 🌟 Pro Tips

1. **Better Predictions**: Update students multiple times to build history
2. **Subject Flexibility**: Add any subject name - system auto-detects
3. **Keyboard Shortcuts**: Click example commands to auto-fill
4. **Graph Types**: Try different visualizations from buttons
5. **Natural Language**: Commands are flexible - try variations!

---

## 📞 Need Help?

Check the README.md for:
- Full API documentation
- Technical details
- Customization guide
- Advanced features

---

**Happy Teaching! 🎓📊✨**
