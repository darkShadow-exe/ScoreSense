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
    if any(phrase in text for phrase in ['add exam', 'add complete exam', 'add test', 'new exam', 
                                           'record exam', 'enter exam', 'submit exam', 'input exam',
                                           'add marks', 'enter marks', 'record marks', 'submit marks',
                                           'give exam', 'enter test', 'record test results']):
        return parse_add_exam(text)
    
    # Intent: ADD_STUDENT (profile only)
    elif any(word in text for word in ['add student', 'create student', 'new student', 'register student',
                                        'enroll student', 'admit student', 'enrol', 'register new',
                                        'i want to add', 'i want to register', 'i want to enroll',
                                        'can you add', 'please add', 'create new student']):
        return parse_add_student_profile(text)
    
    # Intent: UPDATE_STUDENT
    elif any(word in text for word in ['update', 'edit', 'modify', 'change', 'correct', 'fix',
                                        'adjust', 'revise', 'set', 'alter']):
        return parse_update_student(text)
    
    # Intent: DELETE_STUDENT
    elif any(word in text for word in ['delete', 'remove', 'drop', 'eliminate', 'erase',
                                        'take out', 'get rid of']):
        return parse_delete_student(text)
    
    # Intent: SHOW_TOPPER
    elif any(word in text for word in ['topper', 'best student', 'highest', 'top student',
                                        'first rank', 'rank 1', 'who scored highest', 'who is first',
                                        'who got the best', 'best performer', 'top scorer',
                                        'highest scorer', 'who came first', 'number one']):
        return parse_show_topper(text)
    
    # Intent: SHOW_STATS
    elif any(word in text for word in ['average', 'stats', 'statistics', 'class average',
                                        'mean score', 'class performance', 'overall performance',
                                        'class data', 'analytics', 'summary', 'report']):
        return parse_show_stats(text)
    
    # Intent: PREDICT
    elif any(word in text for word in ['predict', 'forecast', 'next score', 'future score',
                                        'expected score', 'what will', 'estimate', 'projection',
                                        'anticipate', 'likely score', 'probable score']):
        return parse_predict(text)
    
    # Intent: COMPARE
    elif any(word in text for word in ['compare', 'comparison', 'rank', 'ranking', 'leaderboard',
                                        'versus', 'vs', 'contrast', 'who is better', 'standings']):
        return parse_compare(text)
    
    # Intent: SHOW_STUDENT
    elif any(word in text for word in ['show', 'display', 'get', 'find', 'search', 'lookup',
                                        'view', 'see', 'info', 'information', 'details', 'tell me about',
                                        'who is', 'what about']):
        return parse_show_student(text)
    
    else:
        return {
            'intent': 'UNKNOWN',
            'error': 'Could not understand the command. Try: "Add student John in grade 10 section A", "Add exam for John: Midterm with math 90, physics 85", "Show class topper", "Predict Sarah\'s math score"'
        }

def extract_name(text):
    """Extract student name from text."""
    # Pattern priority: more specific patterns first
    patterns = [
        # "record test results for NAME:" or "record marks for NAME"
        r'(?:record|enter|submit)\s+(?:test results|marks|exam)\s+(?:for|of)\s+([A-Za-z\s]+?)(?::|\s+with|\s+in)',
        # "add/new exam for NAME:" or "add test for NAME:"
        r'(?:add|new|give)\s+(?:exam|test|complete exam|marks)\s+(?:for|of)\s+([A-Za-z\s]+?)(?::|\s+with|\s+in)',
        # "add student NAME" with optional "can you", "please", "i want to"
        r'(?:add|create|new|register|enroll|enrol|admit)\s+(?:student|new)?\s*([A-Za-z\s]+?)(?:\s+(?:please|in|with|to|grade|section|age|gender|email|phone)|\?|$)',
        # "can you add student NAME" or "i want to register NAME"
        r'(?:can you|please|i want to)\s+(?:add|create|register|enroll)\s+(?:student)?\s*([A-Za-z\s]+?)(?:\s+(?:in|with|to|grade|section|please)|\?|$)',
        # "update/fix/correct NAME's subject to score" or "fix NAME's subject score to score"
        r'(?:update|edit|modify|change|correct|fix|adjust)\s+([A-Za-z]+)\'s\s+[a-z]+\s+(?:score)?\s*(?:to)?\s*\d+',
        # "update/edit/modify/change NAME with"
        r'(?:update|edit|modify|change|correct|fix|adjust|revise|set)\s+([A-Za-z]+)(?:\s+with)',
        # "update/edit/modify/change NAME subject"
        r'(?:update|edit|modify|change|correct|fix|adjust)\s+([A-Za-z]+)\s+[a-z]+\s+\d+',
        # "who is NAME?" or "what about NAME?"
        r'(?:who is|what about|tell me about|info about|information about)\s+([A-Za-z\s]+?)(?:\'s|\?|$)',
        # "expected score for NAME" (avoid capturing 'score')
        r'(?:expected|likely|probable)\s+score\s+for\s+([A-Za-z]+)',
        # "predict/forecast NAME's" - exact possessive match (no spaces before 's)
        r'(?:predict|forecast|estimate|what will)\s+([A-Za-z]+)\'s',
        # "predict/forecast NAME subject"
        r'(?:predict|forecast|estimate)\s+([A-Za-z]+)\s+[a-z]+',
        # "show/display/get/find NAME" (but not "show topper" or "show stats")
        r'(?:show|display|get|find|search|view|see|lookup)\s+(?:me)?\s*(?:info|information|details)?\s*(?:about)?\s*(?!topper|stats|statistics|average|class|me|the|rank|overall|summary|performance|rid)([A-Za-z\s]+?)(?:\s|\?|$)',
        # "get rid of NAME" - specific pattern to avoid capturing 'rid'
        r'get\s+rid\s+of\s+(?:student)?\s*([A-Za-z\s]+?)(?:\s|$)',
        # "delete/remove NAME" or "delete student NAME"
        r'(?:delete|remove|drop|eliminate|erase)(?:\s+student)?\s+([A-Za-z\s]+?)(?:\s|$)',
        # "for NAME" (general case)
        r'(?:for|of|about)\s+([A-Za-z\s]+?)(?:\s+(?:in|with|grade|section|:|exam|\?)|$)',
        # "NAME with" (for commands like "alice with math 90")
        r'^([A-Za-z\s]+?)\s+(?:with|got|scored)',
        # "NAME's" possessive form (fallback, lower priority)
        r'\b([A-Za-z]+)\'s',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Filter out action words and common words that might be captured
            stop_words = ['update', 'edit', 'modify', 'change', 'add', 'new', 'exam', 'test', 
                         'for', 'student', 'what', 'will', 'be', 'the', 'is', 'are', 'predict', 'forecast',
                         'create', 'register', 'enroll', 'enrol', 'admit', 'record', 'enter', 'submit',
                         'delete', 'remove', 'drop', 'show', 'display', 'get', 'find', 'search', 'view',
                         'correct', 'fix', 'adjust', 'revise', 'set', 'me', 'you', 'can', 'please',
                         'want', 'to', 'about', 'of', 'tell', 'who', 'see', 'lookup', 'info', 'information',
                         'details', 'give', 'estimate', 'expected', 'marks', 'complete', 'rid', 'score',
                         'performance', 'results', 'overall', 'summary']
            
            # Split name into words and filter out stop words
            words = name.split()
            filtered_words = [w for w in words if w.lower() not in stop_words]
            
            if filtered_words:
                # Capitalize each word (handles "john doe" -> "John Doe")
                return ' '.join(word.capitalize() for word in filtered_words)
    
    return None

def extract_marks(text):
    """Extract subject-marks pairs from text."""
    marks = {}
    
    # Pattern: "subject to score", "subject score", "score in subject", "subject: score"
    patterns = [
        r'([a-z]+)\s+(?:score)?\s*to\s+(\d+)',  # "math to 95" or "math score to 95"
        r'(\d+)\s+(?:in|for)\s+([a-z]+)',  # "85 in math"
        r'([a-z]+)\s*[:=]\s*(\d+)',  # "math: 85" or "math=85"
        r'([a-z]+)\s+(\d+)',  # "math 85"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Determine if score is first or second based on pattern
            if pattern == patterns[1]:  # "score in subject" - score comes first
                score, subject = match
            else:  # "subject to/: score" - subject comes first
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
