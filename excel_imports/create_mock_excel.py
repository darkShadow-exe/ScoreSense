#!/usr/bin/env python3
"""
Mock Excel File Generator for ScoreSense Import Testing
Creates realistic student exam data in Excel format
"""

import pandas as pd
import random
import os

def create_mock_excel():
    """Create a mock Excel file with student exam data."""
    
    # Student names for realistic data
    students = [
        'Alex Johnson', 'Sarah Wilson', 'Michael Chen', 'Emma Davis', 'Ryan Martinez',
        'Jessica Thompson', 'David Kumar', 'Ashley Brown', 'Christopher Lee', 'Amanda Taylor',
        'Joshua Rodriguez', 'Megan Anderson', 'Tyler Jackson', 'Lauren White', 'Brandon Harris',
        'Samantha Clark', 'Kevin Lewis', 'Nicole Walker', 'Justin Hall', 'Stephanie Young',
        'Austin King', 'Brittany Wright', 'Zachary Lopez', 'Danielle Green', 'Cody Adams'
    ]
    
    # Exam types
    exams = ['Midterm Exam', 'Final Exam', 'Unit Test 1', 'Unit Test 2', 'Quiz 1', 'Quiz 2']
    
    # Subjects
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History']
    
    # Generate realistic data
    data = []
    
    # Create multiple exams for each student
    for student in students:
        # Each student gets 2-3 exams
        num_exams = random.randint(2, 3)
        selected_exams = random.sample(exams, num_exams)
        
        for exam in selected_exams:
            # Each exam has 3-5 subjects
            num_subjects = random.randint(3, 5)
            selected_subjects = random.sample(subjects, num_subjects)
            
            # Create a row with student name, exam, and subject scores
            row = {
                'Student Name': student,
                'Exam': exam
            }
            
            # Performance level for this student (consistent across subjects)
            performance_base = random.choice([
                85,  # Excellent student
                75,  # Good student  
                65,  # Average student
                55,  # Below average student
            ])
            
            # Generate scores for each subject
            for subject in subjects:
                if subject in selected_subjects:
                    # Generate score around performance base with some variation
                    score = performance_base + random.randint(-15, 15)
                    score = max(30, min(100, score))  # Keep within reasonable range
                    row[subject] = score
                else:
                    row[subject] = ''  # Empty for subjects not taken
            
            data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel file
    excel_file = 'mock_student_data.xlsx'
    df.to_excel(excel_file, index=False, sheet_name='Student Exam Data')
    
    print(f"✅ Created mock Excel file: {excel_file}")
    print(f"📊 Contains {len(data)} exam records for {len(students)} students")
    print(f"🏫 Subjects: {', '.join(subjects)}")
    print(f"📝 Exam types: {', '.join(exams)}")
    
    # Display sample data
    print(f"\n📋 Sample Data Preview:")
    print("="*80)
    print(df.head(10).to_string(index=False))
    
    # Create a second Excel file with different structure for testing
    create_alternative_format_excel()
    
    return excel_file

def create_alternative_format_excel():
    """Create another Excel file with different structure."""
    
    # Different format - Class roster with single exam
    students_data = [
        ['John Smith', 'Final Exam', 92, 88, 85, 90, 87],
        ['Mary Johnson', 'Final Exam', 78, 82, 79, 85, 80],
        ['Robert Brown', 'Final Exam', 95, 92, 94, 88, 91],
        ['Lisa Davis', 'Final Exam', 67, 70, 68, 72, 69],
        ['William Wilson', 'Final Exam', 84, 86, 83, 87, 85],
        ['Jennifer Miller', 'Final Exam', 91, 89, 92, 86, 90],
        ['James Anderson', 'Final Exam', 73, 75, 71, 77, 74],
        ['Susan Taylor', 'Final Exam', 88, 85, 87, 89, 86],
        ['Thomas Moore', 'Final Exam', 79, 81, 78, 83, 80],
        ['Karen Thomas', 'Final Exam', 96, 94, 95, 92, 97]
    ]
    
    columns = ['Student Name', 'Exam', 'Math', 'Science', 'English', 'History', 'Geography']
    df2 = pd.DataFrame(students_data, columns=columns)
    
    excel_file2 = 'class_final_exam.xlsx'
    df2.to_excel(excel_file2, index=False, sheet_name='Class Final Results')
    
    print(f"\n✅ Created alternative format Excel: {excel_file2}")
    print(f"📊 Contains final exam results for {len(students_data)} students")
    print(f"\n📋 Alternative Format Preview:")
    print("="*80)
    print(df2.to_string(index=False))

def create_problematic_excel():
    """Create an Excel file with common formatting issues to test error handling."""
    
    problematic_data = [
        ['Student Name', 'Exam', 'Math', 'Science', 'English'],
        ['', '', '', '', ''],  # Empty row
        ['Alice Cooper', 'Test 1', 85, 'N/A', 92],  # Non-numeric score
        ['Bob Dylan', 'Test 1', 78, 82, ''],  # Missing score
        ['Charlie Brown', '', 91, 88, 95],  # Missing exam name
        ['', 'Test 1', 75, 80, 85],  # Missing student name
        ['Diana Ross', 'Test 1', 150, 88, -10],  # Invalid scores (out of range)
        ['Eva Green', 'Test 1', 89.5, 92.3, 87.8],  # Decimal scores (should work)
    ]
    
    df3 = pd.DataFrame(problematic_data[1:], columns=problematic_data[0])
    excel_file3 = 'problematic_data.xlsx'
    df3.to_excel(excel_file3, index=False, sheet_name='Test Data')
    
    print(f"\n⚠️  Created problematic Excel for testing: {excel_file3}")
    print("Contains various formatting issues to test error handling")

def main():
    """Generate all mock Excel files."""
    print("📊 ScoreSense Mock Excel Generator")
    print("="*50)
    
    # Create main mock file
    main_file = create_mock_excel()
    
    # Create problematic file for error testing
    create_problematic_excel()
    
    print(f"\n🎯 Files created in current directory:")
    print(f"   1. {main_file} - Main test file with realistic data")
    print(f"   2. class_final_exam.xlsx - Alternative format")
    print(f"   3. problematic_data.xlsx - Error testing file")
    
    print(f"\n💡 Usage:")
    print(f"   1. Go to http://localhost:5000/students")
    print(f"   2. Click 'Import Excel' button")
    print(f"   3. Upload one of the generated files")
    print(f"   4. Test the import functionality")

if __name__ == '__main__':
    main()