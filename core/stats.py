from models.student_model import get_all_students, get_all_subjects
import statistics

def get_class_average():
    """Calculate overall class average across all subjects."""
    students = get_all_students()
    
    if not students:
        return 0
    
    total_scores = []
    for student in students:
        scores = list(student['marks'].values())
        total_scores.extend(scores)
    
    return round(statistics.mean(total_scores), 2) if total_scores else 0

def get_subject_averages():
    """Calculate average score for each subject."""
    students = get_all_students()
    subjects = get_all_subjects()
    
    subject_scores = {subject: [] for subject in subjects}
    
    for student in students:
        for subject, score in student['marks'].items():
            if subject in subject_scores:
                subject_scores[subject].append(score)
    
    averages = {}
    for subject, scores in subject_scores.items():
        if scores:
            averages[subject] = round(statistics.mean(scores), 2)
    
    return averages

def get_class_topper(subject=None):
    """
    Get the student with highest score.
    If subject is specified, get topper for that subject.
    Otherwise, get overall topper based on average.
    """
    students = get_all_students()
    
    if not students:
        return None
    
    if subject:
        # Subject-specific topper
        best_student = None
        best_score = -1
        
        for student in students:
            if subject in student['marks']:
                score = student['marks'][subject]
                if score > best_score:
                    best_score = score
                    best_student = {
                        'name': student['name'],
                        'score': score,
                        'subject': subject
                    }
        
        return best_student
    else:
        # Overall topper based on average
        best_student = None
        best_avg = -1
        
        for student in students:
            scores = list(student['marks'].values())
            avg = statistics.mean(scores) if scores else 0
            
            if avg > best_avg:
                best_avg = avg
                best_student = {
                    'name': student['name'],
                    'average': round(avg, 2),
                    'marks': student['marks']
                }
        
        return best_student

def get_lowest_scorer(subject=None):
    """Get the student with lowest score."""
    students = get_all_students()
    
    if not students:
        return None
    
    if subject:
        # Subject-specific lowest
        worst_student = None
        worst_score = float('inf')
        
        for student in students:
            if subject in student['marks']:
                score = student['marks'][subject]
                if score < worst_score:
                    worst_score = score
                    worst_student = {
                        'name': student['name'],
                        'score': score,
                        'subject': subject
                    }
        
        return worst_student
    else:
        # Overall lowest based on average
        worst_student = None
        worst_avg = float('inf')
        
        for student in students:
            scores = list(student['marks'].values())
            avg = statistics.mean(scores) if scores else 0
            
            if avg < worst_avg:
                worst_avg = avg
                worst_student = {
                    'name': student['name'],
                    'average': round(avg, 2),
                    'marks': student['marks']
                }
        
        return worst_student

def get_subject_difficulty():
    """
    Rank subjects by difficulty (lower average = more difficult).
    Returns list of tuples (subject, average) sorted by difficulty.
    """
    averages = get_subject_averages()
    
    # Sort by average (ascending = most difficult first)
    difficulty_ranking = sorted(averages.items(), key=lambda x: x[1])
    
    return difficulty_ranking

def get_student_rank(student_name):
    """Get rank of a student based on overall average."""
    students = get_all_students()
    
    if not students:
        return None
    
    # Calculate averages for all students
    student_averages = []
    for student in students:
        scores = list(student['marks'].values())
        avg = statistics.mean(scores) if scores else 0
        student_averages.append({
            'name': student['name'],
            'average': avg
        })
    
    # Sort by average descending
    student_averages.sort(key=lambda x: x['average'], reverse=True)
    
    # Find rank
    for rank, student in enumerate(student_averages, 1):
        if student['name'].lower() == student_name.lower():
            return {
                'rank': rank,
                'total': len(student_averages),
                'average': round(student['average'], 2)
            }
    
    return None

def get_score_distribution():
    """Get distribution of scores in ranges."""
    students = get_all_students()
    
    ranges = {
        '0-40': 0,
        '41-60': 0,
        '61-80': 0,
        '81-100': 0
    }
    
    for student in students:
        for score in student['marks'].values():
            if score <= 40:
                ranges['0-40'] += 1
            elif score <= 60:
                ranges['41-60'] += 1
            elif score <= 80:
                ranges['61-80'] += 1
            else:
                ranges['81-100'] += 1
    
    return ranges

def get_all_stats():
    """Get comprehensive statistics."""
    students = get_all_students()
    
    if not students:
        return {
            'total_students': 0,
            'class_average': 0,
            'subject_averages': {},
            'topper': None,
            'lowest': None,
            'difficulty_ranking': []
        }
    
    return {
        'total_students': len(students),
        'class_average': get_class_average(),
        'subject_averages': get_subject_averages(),
        'topper': get_class_topper(),
        'lowest': get_lowest_scorer(),
        'difficulty_ranking': get_subject_difficulty(),
        'score_distribution': get_score_distribution()
    }

def compare_subject_scores(subject):
    """Get all students' scores in a specific subject for comparison."""
    students = get_all_students()
    
    comparisons = []
    for student in students:
        if subject in student['marks']:
            comparisons.append({
                'name': student['name'],
                'score': student['marks'][subject]
            })
    
    # Sort by score descending
    comparisons.sort(key=lambda x: x['score'], reverse=True)
    
    return comparisons
