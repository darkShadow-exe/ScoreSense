import re
import json

def parse_command(text):
    """
    Parse natural language command and extract intent, name, and marks.
    
    Returns:
        dict with 'intent', 'name', 'marks', 'subject', 'error' keys
    """
    text = text.strip().lower()
    
    # Intent: ADD_EXAM (must check before ADD_STUDENT)
    if any(phrase in text for phrase in ['add exam', 'add complete exam', 'add test', 'new exam']):
        return parse_add_exam(text)
    
    # Intent: ADD_STUDENT (profile only)
    elif any(word in text for word in ['add student', 'create student', 'new student', 'register student']):
        return parse_add_student_profile(text)
    
    # Intent: UPDATE_STUDENT
    elif any(word in text for word in ['update', 'edit', 'modify', 'change']):
        return parse_update_student(text)
    
    # Intent: DELETE_STUDENT
    elif any(word in text for word in ['delete', 'remove']):
        return parse_delete_student(text)
    
    # Intent: SHOW_TOPPER
    elif any(word in text for word in ['topper', 'best student', 'highest', 'top student']):
        return parse_show_topper(text)
    
    # Intent: SHOW_STATS
    elif any(word in text for word in ['average', 'stats', 'statistics', 'class average']):
        return parse_show_stats(text)
    
    # Intent: PREDICT
    elif any(word in text for word in ['predict', 'forecast', 'next score']):
        return parse_predict(text)
    
    # Intent: COMPARE
    elif any(word in text for word in ['compare', 'comparison']):
        return parse_compare(text)
    
    # Intent: SHOW_STUDENT
    elif any(word in text for word in ['show', 'display', 'get', 'find']):
        return parse_show_student(text)
    
    else:
        return {
            'intent': 'UNKNOWN',
            'error': 'Could not understand the command. Try: "Add student John in grade 10 section A", "Add exam for John: Midterm with math 90, physics 85", "Show class topper", "Predict Sarah\'s math score"'
        }

def extract_name(text):
    """Extract student name from text."""
    # Pattern: "add NAME with" or "NAME with" or after "student NAME"
    patterns = [
        r'(?:add|create|new student)\s+([A-Za-z]+)',
        r'([A-Za-z]+)\s+with',
        r'(?:student|for)\s+([A-Za-z]+)',
        r'(?:predict|show|delete|remove|update)\s+([A-Za-z]+)(?:\'s)?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
    
    return None

def extract_marks(text):
    """Extract subject-marks pairs from text."""
    marks = {}
    
    # Pattern: "85 in math", "math 85", "physics: 90"
    patterns = [
        r'(\d+)\s+(?:in|for)\s+([a-z]+)',
        r'([a-z]+)\s*[:=]\s*(\d+)',
        r'([a-z]+)\s+(\d+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if pattern == patterns[0]:  # score comes first
                score, subject = match
            else:  # subject comes first
                subject, score = match
            
            # Validate subject name
            if len(subject) > 2 and subject.isalpha():
                marks[subject.lower()] = int(score)
    
    return marks

def extract_subject(text):
    """Extract a single subject from text."""
    # Common subjects
    subjects = ['math', 'physics', 'chemistry', 'biology', 'english', 'history', 
                'geography', 'computer', 'science', 'social']
    
    for subject in subjects:
        if subject in text:
            return subject
    
    # Try to extract any subject-like word
    match = re.search(r'in\s+([a-z]+)', text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    
    return None

def extract_profile_fields(text):
    """Extract profile fields like grade, section, age, gender from text."""
    profile = {}
    
    # Extract grade: "grade 10", "in grade 11"
    grade_match = re.search(r'(?:in\s+)?grade\s+(\d+|[a-z]+)', text, re.IGNORECASE)
    if grade_match:
        profile['grade'] = grade_match.group(1)
    
    # Extract section: "section A", "section B"
    section_match = re.search(r'section\s+([a-z])', text, re.IGNORECASE)
    if section_match:
        profile['section'] = section_match.group(1).upper()
    
    # Extract age: "age 15", "15 years old"
    age_match = re.search(r'(?:age\s+)?(\d+)(?:\s+years)?', text)
    if age_match:
        profile['age'] = int(age_match.group(1))
    
    # Extract gender: "male", "female"
    if 'male' in text and 'female' not in text:
        profile['gender'] = 'Male'
    elif 'female' in text:
        profile['gender'] = 'Female'
    
    # Extract email: basic pattern
    email_match = re.search(r'([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})', text, re.IGNORECASE)
    if email_match:
        profile['email'] = email_match.group(1)
    
    # Extract phone: 10 digits
    phone_match = re.search(r'(\d{10})', text)
    if phone_match:
        profile['phone'] = phone_match.group(1)
    
    return profile

def extract_exam_name(text):
    """Extract exam name from text."""
    # Pattern: "exam NAME with", "test NAME:", after "for NAME:"
    patterns = [
        r'exam\s+([a-z\s]+?)(?:with|:)',
        r'test\s+([a-z\s]+?)(?:with|:)',
        r'for\s+[a-z]+:\s*([a-z\s]+?)(?:with|:)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            exam_name = match.group(1).strip()
            if len(exam_name) > 2:
                return exam_name.title()
    
    return 'General Exam'

def parse_add_student_profile(text):
    """Parse ADD_STUDENT command (profile only, no exams)."""
    name = extract_name(text)
    profile = extract_profile_fields(text)
    
    if not name:
        return {'intent': 'ADD_STUDENT', 'error': 'Could not extract student name'}
    
    return {
        'intent': 'ADD_STUDENT',
        'name': name,
        'grade': profile.get('grade', ''),
        'section': profile.get('section', ''),
        'age': profile.get('age', ''),
        'gender': profile.get('gender', ''),
        'email': profile.get('email', ''),
        'phone': profile.get('phone', ''),
        'address': ''  # Not extractable from simple commands
    }

def parse_add_exam(text):
    """Parse ADD_EXAM command (add complete exam with all subjects)."""
    name = extract_name(text)
    exam_name = extract_exam_name(text)
    marks = extract_marks(text)
    
    if not name:
        return {'intent': 'ADD_EXAM', 'error': 'Could not extract student name'}
    
    if not marks:
        return {'intent': 'ADD_EXAM', 'error': 'Could not extract marks. Use format: "Add exam for John: Midterm with math 90, physics 85"'}
    
    return {
        'intent': 'ADD_EXAM',
        'name': name,
        'exam_name': exam_name,
        'marks': marks
    }

def parse_update_student(text):
    """Parse UPDATE_STUDENT command."""
    name = extract_name(text)
    marks = extract_marks(text)
    
    if not name:
        return {'intent': 'UPDATE_STUDENT', 'error': 'Could not extract student name'}
    
    if not marks:
        return {'intent': 'UPDATE_STUDENT', 'error': 'Could not extract marks to update'}
    
    return {
        'intent': 'UPDATE_STUDENT',
        'name': name,
        'marks': marks
    }

def parse_delete_student(text):
    """Parse DELETE_STUDENT command."""
    name = extract_name(text)
    
    if not name:
        return {'intent': 'DELETE_STUDENT', 'error': 'Could not extract student name'}
    
    return {
        'intent': 'DELETE_STUDENT',
        'name': name
    }

def parse_show_student(text):
    """Parse SHOW_STUDENT command."""
    name = extract_name(text)
    
    if not name:
        return {'intent': 'SHOW_STUDENT', 'error': 'Could not extract student name'}
    
    return {
        'intent': 'SHOW_STUDENT',
        'name': name
    }

def parse_show_topper(text):
    """Parse SHOW_TOPPER command."""
    subject = extract_subject(text)
    
    return {
        'intent': 'SHOW_TOPPER',
        'subject': subject  # None means overall topper
    }

def parse_show_stats(text):
    """Parse SHOW_STATS command."""
    subject = extract_subject(text)
    
    return {
        'intent': 'SHOW_STATS',
        'subject': subject  # None means overall stats
    }

def parse_predict(text):
    """Parse PREDICT command."""
    name = extract_name(text)
    subject = extract_subject(text)
    
    if not name:
        return {'intent': 'PREDICT', 'error': 'Could not extract student name'}
    
    if not subject:
        return {'intent': 'PREDICT', 'error': 'Could not extract subject. Use format: "Predict John\'s math score"'}
    
    return {
        'intent': 'PREDICT',
        'name': name,
        'subject': subject
    }

def parse_compare(text):
    """Parse COMPARE command."""
    subject = extract_subject(text)
    
    return {
        'intent': 'COMPARE',
        'subject': subject  # None means compare all subjects
    }

# Test examples
if __name__ == '__main__':
    test_commands = [
        "Add student Krish in grade 10 section A",
        "Add exam for Krish: Midterm with math 95, physics 80, chemistry 88",
        "Show me the class topper",
        "Predict Sneha's next math score",
        "Compare scores of the class in chemistry",
        "Update John's email to john@school.com",
        "Delete Sarah",
        "Show class average",
    ]
    
    for cmd in test_commands:
        print(f"\nCommand: {cmd}")
        print(f"Result: {json.dumps(parse_command(cmd), indent=2)}")
