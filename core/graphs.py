import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
from models.student_model import get_all_students, get_student_by_name
from core.stats import get_subject_averages, get_score_distribution, compare_subject_scores

def generate_student_bar(student_name):
    """
    Generate bar chart for a single student's subject scores.
    Returns base64 encoded image.
    """
    from models.student_model import get_student_by_name
    
    student = get_student_by_name(student_name)
    if not student:
        return None
    
    subjects = list(student['marks'].keys())
    scores = list(student['marks'].values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(subjects, scores, color='#4CAF50', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Subjects', fontsize=12)
    plt.ylabel('Scores', fontsize=12)
    plt.title(f"{student['name']}'s Scores by Subject", fontsize=14, fontweight='bold')
    plt.ylim(0, 105)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # Convert to base64
    img_data = fig_to_base64()
    plt.close()
    
    return img_data

def generate_subject_average_bar():
    """
    Generate bar chart showing class average for each subject.
    Returns base64 encoded image.
    """
    averages = get_subject_averages()
    
    if not averages:
        return None
    
    subjects = list(averages.keys())
    avg_scores = list(averages.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(subjects, avg_scores, color='#2196F3', alpha=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Subjects', fontsize=12)
    plt.ylabel('Average Score', fontsize=12)
    plt.title('Class Average by Subject', fontsize=14, fontweight='bold')
    plt.ylim(0, 105)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    img_data = fig_to_base64()
    plt.close()
    
    return img_data

def generate_distribution_histogram():
    """
    Generate histogram showing score distribution across ranges.
    Returns base64 encoded image.
    """
    distribution = get_score_distribution()
    
    ranges = list(distribution.keys())
    counts = list(distribution.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(ranges, counts, color='#FF9800', alpha=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Score Range', fontsize=12)
    plt.ylabel('Number of Scores', fontsize=12)
    plt.title('Score Distribution', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    img_data = fig_to_base64()
    plt.close()
    
    return img_data

def generate_comparison_chart(subject):
    """
    Generate bar chart comparing all students' scores in a subject.
    Returns base64 encoded image.
    """
    comparisons = compare_subject_scores(subject)
    
    if not comparisons:
        return None
    
    names = [c['name'] for c in comparisons]
    scores = [c['score'] for c in comparisons]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(names, scores, color='#9C27B0', alpha=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9)
    
    plt.xlabel('Students', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title(f'Class Comparison - {subject.capitalize()}', fontsize=14, fontweight='bold')
    plt.ylim(0, 105)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    img_data = fig_to_base64()
    plt.close()
    
    return img_data

def generate_student_comparison():
    """
    Generate grouped bar chart comparing all students across all subjects.
    Returns base64 encoded image.
    """
    students = get_all_students()
    
    if not students:
        return None
    
    # Get all unique subjects
    all_subjects = set()
    for student in students:
        all_subjects.update(student['marks'].keys())
    all_subjects = sorted(list(all_subjects))
    
    # Prepare data
    student_names = [s['name'] for s in students]
    
    import numpy as np
    x = np.arange(len(student_names))
    width = 0.8 / len(all_subjects) if all_subjects else 0.8
    
    plt.figure(figsize=(14, 7))
    
    # Create bars for each subject
    colors = ['#F44336', '#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4']
    
    for i, subject in enumerate(all_subjects):
        scores = []
        for student in students:
            scores.append(student['marks'].get(subject, 0))
        
        offset = width * i - (width * len(all_subjects) / 2) + width/2
        plt.bar(x + offset, scores, width, label=subject.capitalize(), 
                color=colors[i % len(colors)], alpha=0.8)
    
    plt.xlabel('Students', fontsize=12)
    plt.ylabel('Scores', fontsize=12)
    plt.title('Student Performance Comparison', fontsize=14, fontweight='bold')
    plt.xticks(x, student_names, rotation=45, ha='right')
    plt.legend()
    plt.ylim(0, 105)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    img_data = fig_to_base64()
    plt.close()
    
    return img_data

def generate_trend_chart(student_name, subject):
    """
    Generate line chart showing score trend for a student in a subject.
    Returns base64 encoded image.
    """
    from models.student_model import get_student_by_name, get_student_history
    
    student = get_student_by_name(student_name)
    if not student:
        return None
    
    history = get_student_history(student['id'], subject)
    
    if len(history) < 2:
        return None
    
    dates = [h['date'] for h in history]
    scores = [h['score'] for h in history]
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(scores) + 1), scores, marker='o', linewidth=2, 
             markersize=8, color='#4CAF50')
    
    # Add value labels
    for i, score in enumerate(scores):
        plt.text(i + 1, score + 2, f'{int(score)}', ha='center', fontsize=10)
    
    plt.xlabel('Exam Number', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title(f"{student_name}'s {subject.capitalize()} Score Trend", 
              fontsize=14, fontweight='bold')
    plt.ylim(0, 105)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    img_data = fig_to_base64()
    plt.close()
    
    return img_data

def fig_to_base64():
    """Convert current matplotlib figure to base64 string."""
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode()
    return img_str
