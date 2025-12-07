import re
import json

def parse_command(text):
    """
    Parse natural language command and extract intent, name, and marks.
    
    Returns:
        dict with 'intent', 'name', 'marks', 'subject', 'error' keys
    """
    text = text.strip().lower()
    
    # Intent: ADD_STUDENT
    if any(word in text for word in ['add', 'create', 'insert', 'new student']):
        return parse_add_student(text)
    
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
            'error': 'Could not understand the command. Try commands like: "Add John with 90 in math", "Show class topper", "Predict Sarah\'s math score"'
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

def parse_add_student(text):
    """Parse ADD_STUDENT command."""
    name = extract_name(text)
    marks = extract_marks(text)
    
    if not name:
        return {'intent': 'ADD_STUDENT', 'error': 'Could not extract student name'}
    
    if not marks:
        return {'intent': 'ADD_STUDENT', 'error': 'Could not extract marks. Use format: "Add John with 90 in math and 85 in physics"'}
    
    return {
        'intent': 'ADD_STUDENT',
        'name': name,
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
        "Add Krish with 95 in math and 80 in physics",
        "Show me the class topper",
        "Predict Sneha's next math score",
        "Compare scores of the class in chemistry",
        "Update John with 88 in physics",
        "Delete Sarah",
        "Show class average",
    ]
    
    for cmd in test_commands:
        print(f"\nCommand: {cmd}")
        print(f"Result: {json.dumps(parse_command(cmd), indent=2)}")
