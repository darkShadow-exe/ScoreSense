from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.student_model import (
    add_student, get_all_students, get_student_by_id,
    get_student_by_name, update_student, delete_student, get_all_subjects,
    get_all_exams_for_student, add_exam_score, delete_exam, add_complete_exam
)
from core.nlu import parse_command
from core.stats import (
    get_all_stats, get_class_topper, get_subject_averages,
    compare_subject_scores, get_student_rank
)
from core.graphs import (
    generate_student_bar, generate_subject_average_bar,
    generate_distribution_histogram, generate_comparison_chart,
    generate_student_comparison
)
from core.predict import predict_score, predict_improvement_needed, batch_predict

app = Flask(__name__)

@app.route('/')
def index():
    """Dashboard page."""
    stats = get_all_stats()
    return render_template('index.html', stats=stats)

@app.route('/students')
def students():
    """List all students."""
    all_students = get_all_students()
    subjects = get_all_subjects()
    return render_template('student_list.html', students=all_students, subjects=subjects)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add new student with personal details only."""
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        section = request.form.get('section')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if name:
            result = add_student(
                name=name,
                grade=grade,
                section=section,
                age=int(age) if age else None,
                gender=gender,
                email=email,
                phone=phone,
                address=address
            )
            if result:
                return redirect(url_for('students'))
            else:
                error = 'Student already exists'
                return render_template('add_student.html', error=error)
        else:
            error = 'Please provide student name'
            return render_template('add_student.html', error=error)
    
    return render_template('add_student.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    """Edit student information and add new exam scores."""
    from models.student_model import get_exams_grouped_by_name
    
    student = get_student_by_id(student_id)
    
    if not student:
        return redirect(url_for('students'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        section = request.form.get('section')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        update_student(
            student_id,
            name=name if name else None,
            grade=grade if grade else None,
            section=section if section else None,
            age=int(age) if age else None,
            gender=gender if gender else None,
            email=email if email else None,
            phone=phone if phone else None,
            address=address if address else None
        )
        
        return redirect(url_for('students'))
    
    # Get existing exams for display
    exams = get_exams_grouped_by_name(student_id)
    
    return render_template('edit_student.html', student=student, exams=exams)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete(student_id):
    """Delete a student."""
    delete_student(student_id)
    return redirect(url_for('students'))

@app.route('/stats')
def stats():
    """Show comprehensive statistics."""
    all_stats = get_all_stats()
    # Get all students sorted by average for top performers
    all_students = get_all_students()
    # Sort by average descending
    all_students.sort(key=lambda x: x.get('average', 0), reverse=True)
    return render_template('stats.html', stats=all_stats, students=all_students)

@app.route('/command', methods=['GET', 'POST'])
def command():
    """Natural language command interface."""
    result = None
    error = None
    
    if request.method == 'POST':
        text = request.form.get('command', '').strip()
        
        if text:
            parsed = parse_command(text)
            result = execute_command(parsed)
        else:
            error = 'Please enter a command'
    
    return render_template('command.html', result=result, error=error)

def execute_command(parsed):
    """Execute parsed NLU command and return result."""
    intent = parsed.get('intent')
    
    if 'error' in parsed:
        return {'error': parsed['error'], 'intent': intent}
    
    # ADD_STUDENT (profile only)
    if intent == 'ADD_STUDENT':
        name = parsed['name']
        grade = parsed.get('grade', '')
        section = parsed.get('section', '')
        age = parsed.get('age', '')
        gender = parsed.get('gender', '')
        email = parsed.get('email', '')
        phone = parsed.get('phone', '')
        address = parsed.get('address', '')
        
        student_id = add_student(name, grade, section, age, gender, email, phone, address)
        if student_id:
            profile_info = f" (Grade: {grade}, Section: {section})" if grade or section else ""
            return {
                'success': True,
                'message': f'Successfully added student {name}{profile_info}. You can now add exams for this student.',
                'student': {'name': name, 'grade': grade, 'section': section}
            }
        else:
            return {'error': f'Student {name} already exists'}
    
    # ADD_EXAM (add complete exam for existing student)
    elif intent == 'ADD_EXAM':
        name = parsed['name']
        exam_name = parsed['exam_name']
        marks = parsed['marks']
        
        student = get_student_by_name(name)
        if student:
            add_complete_exam(student['id'], exam_name, marks)
            return {
                'success': True,
                'message': f'Successfully added {exam_name} for {name} with marks: {marks}',
                'student': {'name': name, 'exam_name': exam_name, 'marks': marks}
            }
        else:
            return {'error': f'Student {name} not found. Please add the student first.'}
    
    # UPDATE_STUDENT
    elif intent == 'UPDATE_STUDENT':
        name = parsed['name']
        marks = parsed.get('marks', {})
        
        student = get_student_by_name(name)
        if student:
            # Check if profile fields are being updated
            profile_fields = {}
            for field in ['grade', 'section', 'age', 'gender', 'email', 'phone', 'address']:
                if field in parsed and parsed[field]:
                    profile_fields[field] = parsed[field]
            
            if profile_fields:
                # Update profile
                update_student(student['id'], **profile_fields)
                return {
                    'success': True,
                    'message': f'Updated {name}\'s profile: {profile_fields}',
                    'student': {'name': name, 'updates': profile_fields}
                }
            elif marks:
                # Add new exam with updated marks
                add_complete_exam(student['id'], 'Voice Update', marks)
                return {
                    'success': True,
                    'message': f'Added new exam for {name} with marks: {marks}',
                    'student': {'name': name, 'marks': marks}
                }
            else:
                return {'error': 'No update information provided'}
        else:
            return {'error': f'Student {name} not found'}
    
    # DELETE_STUDENT
    elif intent == 'DELETE_STUDENT':
        name = parsed['name']
        student = get_student_by_name(name)
        
        if student:
            delete_student(student['id'])
            return {
                'success': True,
                'message': f'Deleted student {name}'
            }
        else:
            return {'error': f'Student {name} not found'}
    
    # SHOW_STUDENT
    elif intent == 'SHOW_STUDENT':
        name = parsed['name']
        student = get_student_by_name(name)
        
        if student:
            rank_info = get_student_rank(name)
            return {
                'success': True,
                'student': student,
                'rank': rank_info
            }
        else:
            return {'error': f'Student {name} not found'}
    
    # SHOW_TOPPER
    elif intent == 'SHOW_TOPPER':
        subject = parsed.get('subject')
        topper = get_class_topper(subject)
        
        if topper:
            return {
                'success': True,
                'topper': topper,
                'subject': subject or 'Overall'
            }
        else:
            return {'error': 'No students found'}
    
    # SHOW_STATS
    elif intent == 'SHOW_STATS':
        subject = parsed.get('subject')
        
        if subject:
            avg = get_subject_averages().get(subject)
            comparisons = compare_subject_scores(subject)
            
            return {
                'success': True,
                'subject': subject,
                'average': avg,
                'comparisons': comparisons
            }
        else:
            stats = get_all_stats()
            return {
                'success': True,
                'stats': stats
            }
    
    # PREDICT
    elif intent == 'PREDICT':
        name = parsed['name']
        subject = parsed['subject']
        
        prediction = predict_score(name, subject)
        
        if 'error' not in prediction:
            return {
                'success': True,
                'prediction': prediction,
                'student': name,
                'subject': subject
            }
        else:
            return {'error': prediction['error']}
    
    # COMPARE
    elif intent == 'COMPARE':
        subject = parsed.get('subject')
        
        if subject:
            comparisons = compare_subject_scores(subject)
            avg = get_subject_averages().get(subject)
            
            return {
                'success': True,
                'comparisons': comparisons,
                'subject': subject,
                'average': avg
            }
        else:
            return {'error': 'Please specify a subject to compare'}
    
    return {'error': 'Unknown intent'}

@app.route('/graph/<graph_type>')
def graph(graph_type):
    """Generate and return graph as base64 image."""
    from core.graphs import (generate_student_bar, generate_subject_average_bar, 
                            generate_distribution_histogram, generate_comparison_chart,
                            generate_student_comparison, generate_student_pie,
                            generate_student_line, generate_student_radar)
    
    student_name = request.args.get('student')
    subject = request.args.get('subject')
    
    img_data = None
    
    if graph_type == 'student_bar' and student_name:
        img_data = generate_student_bar(student_name)
    elif graph_type == 'student_pie' and student_name:
        img_data = generate_student_pie(student_name)
    elif graph_type == 'student_line' and student_name:
        img_data = generate_student_line(student_name)
    elif graph_type == 'student_radar' and student_name:
        img_data = generate_student_radar(student_name)
    elif graph_type == 'subject_average':
        img_data = generate_subject_average_bar()
    elif graph_type == 'distribution':
        img_data = generate_distribution_histogram()
    elif graph_type == 'comparison' and subject:
        img_data = generate_comparison_chart(subject)
    elif graph_type == 'student_comparison':
        img_data = generate_student_comparison()
    
    if img_data:
        return jsonify({'image': img_data})
    else:
        return jsonify({'error': 'Could not generate graph'}), 400

@app.route('/predict/<student_name>/<subject>')
def predict_endpoint(student_name, subject):
    """API endpoint for prediction."""
    result = predict_score(student_name, subject)
    return jsonify(result)

@app.route('/api/students', methods=['GET'])
def api_students():
    """API endpoint to get all students."""
    students = get_all_students()
    return jsonify(students)

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API endpoint to get statistics."""
    stats = get_all_stats()
    return jsonify(stats)

@app.route('/student/<int:student_id>/exams')
def student_exams(student_id):
    """View all exams for a student."""
    student = get_student_by_id(student_id)
    if not student:
        return redirect(url_for('students'))
    
    exams = get_all_exams_for_student(student_id)
    return jsonify({'student': student, 'exams': exams})

@app.route('/student/<int:student_id>/stats')
def student_stats(student_id):
    """Show detailed statistics for a specific student."""
    from models.student_model import get_student_detailed_stats
    
    stats = get_student_detailed_stats(student_id)
    if not stats:
        return redirect(url_for('students'))
    
    return render_template('student_detail.html', stats=stats)

@app.route('/student/<int:student_id>/add_exam', methods=['POST'])
def add_exam(student_id):
    """Add a new exam score for a student."""
    subject = request.form.get('subject')
    score = request.form.get('score')
    exam_name = request.form.get('exam_name', 'Test')
    
    if subject and score:
        add_exam_score(student_id, subject, float(score), exam_name)
    
    return redirect(url_for('edit', student_id=student_id))

@app.route('/student/<int:student_id>/add_complete_exam', methods=['POST'])
def add_complete_exam_route(student_id):
    """Add a complete exam with all subjects."""
    from models.student_model import add_complete_exam
    
    exam_name = request.form.get('exam_name', 'New Exam')
    marks = {}
    
    for key in request.form:
        if key.startswith('subject_'):
            subject = request.form[key]
            score_key = key.replace('subject_', 'score_')
            score = request.form.get(score_key)
            
            if subject and score:
                marks[subject.lower()] = float(score)
    
    if marks:
        add_complete_exam(student_id, exam_name, marks)
    
    return redirect(url_for('edit', student_id=student_id))

@app.route('/exam/<int:exam_id>/delete', methods=['POST'])
def delete_exam_route(exam_id):
    """Delete an exam record."""
    delete_exam(exam_id)
    return redirect(request.referrer or url_for('students'))

@app.route('/import', methods=['GET', 'POST'])
def import_excel():
    """Import data from Excel file."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('import_excel.html', error='No file uploaded')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('import_excel.html', error='No file selected')
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return render_template('import_excel.html', error='Please upload an Excel file (.xlsx or .xls)')
        
        # Get options
        avoid_duplicates = request.form.get('avoid_duplicates') == 'on'
        
        # Import data
        from core.excel_import import import_excel_from_upload
        stats = import_excel_from_upload(file, avoid_duplicates)
        
        return render_template('import_excel.html', stats=stats)
    
    return render_template('import_excel.html')

if __name__ == '__main__':
    print("Starting Score Analyser Application...")
    print("Access the application at: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
