"""
Excel import functionality with LLM-based structure understanding.
Automatically detects and parses any Excel structure containing student exam data.
"""

import pandas as pd
import json
import re
from models.student_model import (
    get_student_by_name, add_student, add_complete_exam, 
    get_connection
)

def analyze_excel_structure_simple(df):
    """
    Analyze Excel structure using pattern matching (fallback when LLM unavailable).
    Returns parsed data structure.
    """
    # Convert all column names to lowercase for easier matching
    df.columns = [str(col).lower().strip() for col in df.columns]
    
    # Try to identify key columns
    name_col = None
    exam_col = None
    subject_cols = []
    
    # Find name column
    for col in df.columns:
        if any(keyword in col for keyword in ['name', 'student', 'pupil']):
            name_col = col
            break
    
    # Find exam column
    for col in df.columns:
        if any(keyword in col for keyword in ['exam', 'test', 'assessment', 'term', 'semester']):
            exam_col = col
            break
    
    # Find subject columns (numeric columns that aren't ID)
    for col in df.columns:
        if col not in [name_col, exam_col]:
            # Check if column contains numeric data
            try:
                pd.to_numeric(df[col], errors='raise')
                subject_cols.append(col)
            except:
                # Check if it's a subject name
                common_subjects = ['math', 'physics', 'chemistry', 'biology', 'english', 
                                 'history', 'computer', 'science', 'geography']
                if any(subj in col for subj in common_subjects):
                    subject_cols.append(col)
    
    if not name_col:
        raise ValueError("Could not identify student name column")
    
    # Parse the data
    records = []
    for _, row in df.iterrows():
        student_name = str(row[name_col]).strip()
        if not student_name or student_name.lower() in ['nan', 'none', '']:
            continue
        
        exam_name = str(row[exam_col]).strip() if exam_col else 'Imported Exam'
        if exam_name.lower() in ['nan', 'none', '']:
            exam_name = 'Imported Exam'
        
        # Extract subject scores
        scores = {}
        for col in subject_cols:
            try:
                score = float(row[col])
                if 0 <= score <= 100:  # Valid score range
                    # Clean up subject name
                    subject = col.replace('_', ' ').title()
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

def analyze_excel_with_llm(df, api_key=None):
    """
    Use LLM to understand Excel structure.
    Falls back to pattern matching if LLM unavailable.
    """
    try:
        if not api_key:
            # Try to get from environment or config
            import os
            api_key = os.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            print("No API key found, using pattern matching...")
            return analyze_excel_structure_simple(df)
        
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Prepare sample of data for LLM
        sample_data = {
            'columns': list(df.columns),
            'sample_rows': df.head(5).to_dict('records'),
            'shape': df.shape
        }
        
        prompt = f"""You are analyzing an Excel sheet containing student exam data.

Excel Structure:
- Columns: {sample_data['columns']}
- Sample Data (first 5 rows): {json.dumps(sample_data['sample_rows'], indent=2)}
- Total rows: {sample_data['shape'][0]}, Total columns: {sample_data['shape'][1]}

Please analyze this structure and provide a JSON response with:
1. "name_column": The column containing student names
2. "exam_column": The column containing exam/test names (or null if none)
3. "subject_columns": List of columns containing subject scores
4. "structure_type": One of ["wide" (subjects as columns), "long" (subjects as rows)]

Your response must be valid JSON only, no explanations."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing spreadsheet structures for educational data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        analysis = json.loads(response.choices[0].message.content)
        
        # Use LLM analysis to parse data
        return parse_with_llm_analysis(df, analysis)
        
    except Exception as e:
        print(f"LLM analysis failed: {e}, falling back to pattern matching...")
        return analyze_excel_structure_simple(df)

def parse_with_llm_analysis(df, analysis):
    """Parse Excel data using LLM-provided analysis."""
    records = []
    
    name_col = analysis.get('name_column')
    exam_col = analysis.get('exam_column')
    subject_cols = analysis.get('subject_columns', [])
    
    if not name_col:
        raise ValueError("Could not identify name column from LLM analysis")
    
    for _, row in df.iterrows():
        student_name = str(row[name_col]).strip()
        if not student_name or student_name.lower() in ['nan', 'none', '']:
            continue
        
        exam_name = str(row[exam_col]).strip() if exam_col and exam_col in df.columns else 'Imported Exam'
        if not exam_name or exam_name.lower() in ['nan', 'none', '']:
            exam_name = 'Imported Exam'
        
        scores = {}
        for col in subject_cols:
            if col in df.columns:
                try:
                    score = float(row[col])
                    if 0 <= score <= 100:
                        subject = col.replace('_', ' ').title()
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

def import_excel_data(file_path, api_key=None, avoid_duplicates=True):
    """
    Import Excel file and add data to database.
    
    Args:
        file_path: Path to Excel file
        api_key: OpenAI API key (optional, falls back to pattern matching)
        avoid_duplicates: Skip duplicate exam entries
    
    Returns:
        dict with import statistics
    """
    # Read Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return {'error': f'Failed to read Excel file: {str(e)}'}
    
    if df.empty:
        return {'error': 'Excel file is empty'}
    
    # Analyze structure
    try:
        records = analyze_excel_with_llm(df, api_key)
    except Exception as e:
        return {'error': f'Failed to analyze Excel structure: {str(e)}'}
    
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
                # Add new student with basic info
                student_id = add_student(student_name, '', '', '', '', '', '', '')
                stats['students_added'] += 1
            else:
                student_id = student['id']
                stats['students_updated'] += 1
            
            # Add exam data
            exams_added_for_record = 0
            duplicates_in_record = 0
            
            for subject, score in scores.items():
                if avoid_duplicates and check_duplicate_exam(student_id, exam_name, subject):
                    duplicates_in_record += 1
                    continue
                
                # Add individual exam entry
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO exams (student_id, exam_name, subject, score)
                    VALUES (?, ?, ?, ?)
                ''', (student_id, exam_name, subject, score))
                conn.commit()
                conn.close()
                
                exams_added_for_record += 1
            
            stats['exams_added'] += exams_added_for_record
            stats['duplicates_skipped'] += duplicates_in_record
            
        except Exception as e:
            stats['errors'].append(f"Error processing {record.get('student_name', 'unknown')}: {str(e)}")
    
    return stats

def import_excel_from_upload(file, api_key=None, avoid_duplicates=True):
    """
    Import Excel from uploaded file object.
    
    Args:
        file: Werkzeug FileStorage object
        api_key: OpenAI API key
        avoid_duplicates: Skip duplicate exam entries
    
    Returns:
        dict with import statistics
    """
    try:
        # Read directly from file object
        df = pd.read_excel(file)
        
        if df.empty:
            return {'error': 'Excel file is empty'}
        
        # Analyze structure
        records = analyze_excel_with_llm(df, api_key)
        
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
