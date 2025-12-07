"""
Excel import functionality with simple structure parsing.
Expects format: Student Name | Exam | Subject1 | Subject2 | ...
"""

import pandas as pd
from models.student_model import (
    get_student_by_name, add_student, get_connection
)

def parse_excel_structure(df):
    """
    Parse Excel with expected structure:
    Columns: Student Name, Exam, [Subject columns...]
    
    Returns parsed data structure.
    """
    # Expected first two columns: Student Name and Exam
    if len(df.columns) < 3:
        raise ValueError("Excel must have at least 3 columns: Student Name, Exam, and at least one subject")
    
    # Get column names
    name_col = df.columns[0]  # First column is student name
    exam_col = df.columns[1]  # Second column is exam name
    subject_cols = df.columns[2:]  # Rest are subjects
    
    # Parse the data
    records = []
    for _, row in df.iterrows():
        student_name = str(row[name_col]).strip()
        if not student_name or student_name.lower() in ['nan', 'none', '']:
            continue
        
        exam_name = str(row[exam_col]).strip()
        if not exam_name or exam_name.lower() in ['nan', 'none', '']:
            exam_name = 'Imported Exam'
        
        # Extract subject scores
        scores = {}
        for col in subject_cols:
            try:
                score = float(row[col])
                if 0 <= score <= 100:  # Valid score range
                    subject = str(col).strip()
                    scores[subject] = score
            except:
                continue
        
        if scores:
            records.append({
                'student_name': student_name,
                'exam_name': exam_name,
                'scores': scores
            })
    
    return records

def check_duplicate_exam(student_id, exam_name, subject):
    """Check if an exam entry already exists."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM exams
        WHERE student_id = ? AND exam_name = ? AND subject = ?
    ''', (student_id, exam_name, subject))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0

def import_excel_from_upload(file, avoid_duplicates=True):
    """
    Import Excel from uploaded file object.
    
    Expected format:
    Column 1: Student Name
    Column 2: Exam
    Columns 3+: Subjects (with numeric scores)
    
    Args:
        file: Werkzeug FileStorage object
        avoid_duplicates: Skip duplicate exam entries
    
    Returns:
        dict with import statistics
    """
    try:
        # Read directly from file object
        df = pd.read_excel(file)
        
        if df.empty:
            return {'error': 'Excel file is empty'}
        
        if len(df.columns) < 3:
            return {'error': 'Excel must have at least 3 columns: Student Name, Exam, and subject(s)'}
        
        # Parse structure
        try:
            records = parse_excel_structure(df)
        except Exception as e:
            return {'error': f'Failed to parse Excel: {str(e)}'}
        
        if not records:
            return {'error': 'No valid data found in Excel file'}
        
        # Import data
        stats = {
            'total_records': len(records),
            'students_added': 0,
            'students_updated': 0,
            'exams_added': 0,
            'duplicates_skipped': 0,
            'errors': []
        }
        
        for record in records:
            try:
                student_name = record['student_name']
                exam_name = record['exam_name']
                scores = record['scores']
                
                # Get or create student
                student = get_student_by_name(student_name)
                
                if not student:
                    student_id = add_student(student_name, '', '', '', '', '', '', '')
                    stats['students_added'] += 1
                else:
                    student_id = student['id']
                    stats['students_updated'] += 1
                
                # Add exam data
                for subject, score in scores.items():
                    if avoid_duplicates and check_duplicate_exam(student_id, exam_name, subject):
                        stats['duplicates_skipped'] += 1
                        continue
                    
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO exams (student_id, exam_name, subject, score)
                        VALUES (?, ?, ?, ?)
                    ''', (student_id, exam_name, subject, score))
                    conn.commit()
                    conn.close()
                    
                    stats['exams_added'] += 1
                
            except Exception as e:
                stats['errors'].append(f"Error processing {record.get('student_name', 'unknown')}: {str(e)}")
        
        return stats
        
    except Exception as e:
        return {'error': f'Failed to process Excel file: {str(e)}'}
