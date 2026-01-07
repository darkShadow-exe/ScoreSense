# Removed heavy startup import: from sklearn.linear_model import LinearRegression
import numpy as np
from models.student_model import get_student_by_name, get_student_history

def predict_score(student_name, subject):
    """
    Predict next score for a student in a subject using linear regression.
    
    Args:
        student_name: Name of the student
        subject: Subject to predict
    
    Returns:
        dict with 'predicted_score', 'confidence', 'history' or 'error'
    """
    # Lazy import heavy library only when needed
    from sklearn.linear_model import LinearRegression
    
    student = get_student_by_name(student_name)
    
    if not student:
        return {'error': f'Student {student_name} not found'}
    
    # Get historical scores
    history = get_student_history(student['id'], subject)
    
    if not history:
        # No history, use current score as baseline
        if subject in student['marks']:
            current_score = student['marks'][subject]
            return {
                'predicted_score': round(current_score, 2),
                'confidence': 'low',
                'method': 'baseline',
                'message': 'No historical data. Using current score as prediction.'
            }
        else:
            return {'error': f'No data available for {subject}'}
    
    # If only one data point, use heuristic
    if len(history) == 1:
        current_score = history[0]['score']
        class_avg = get_class_average_for_subject(subject)
        
        # Simple heuristic: assume slight improvement toward class average
        predicted = (current_score * 0.7 + class_avg * 0.3)
        
        return {
            'predicted_score': round(predicted, 2),
            'confidence': 'medium',
            'method': 'heuristic',
            'message': 'Limited data. Using heuristic prediction.'
        }
    
    # Use linear regression for multiple data points
    scores = [h['score'] for h in history]
    X = np.array(range(1, len(scores) + 1)).reshape(-1, 1)
    y = np.array(scores)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next score
    next_index = len(scores) + 1
    predicted = model.predict([[next_index]])[0]
    
    # Calculate R² score for confidence
    r2_score = model.score(X, y)
    
    # Clamp prediction to valid range
    predicted = max(0, min(100, predicted))
    
    # Determine confidence level
    if r2_score > 0.8:
        confidence = 'high'
    elif r2_score > 0.5:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    return {
        'predicted_score': round(predicted, 2),
        'confidence': confidence,
        'r2_score': round(r2_score, 3),
        'method': 'linear_regression',
        'history_count': len(scores),
        'trend': 'improving' if model.coef_[0] > 0 else 'declining',
        'message': f'Based on {len(scores)} past exams'
    }

def predict_heuristic(student_name, subject):
    """
    Simple heuristic prediction without ML.
    Useful as fallback or for quick estimates.
    """
    student = get_student_by_name(student_name)
    
    if not student:
        return {'error': f'Student {student_name} not found'}
    
    if subject not in student['marks']:
        return {'error': f'No data for {subject}'}
    
    current_score = student['marks'][subject]
    history = get_student_history(student['id'], subject)
    
    if len(history) < 2:
        # Use current score
        predicted = current_score
    else:
        # Average of last score and mean of recent scores
        last_score = history[-1]['score']
        recent_scores = [h['score'] for h in history[-3:]]  # Last 3
        mean_recent = np.mean(recent_scores)
        
        predicted = (last_score + mean_recent) / 2
    
    return {
        'predicted_score': round(predicted, 2),
        'method': 'heuristic',
        'message': 'Simple average-based prediction'
    }

def get_class_average_for_subject(subject):
    """Helper to get class average for a specific subject."""
    from core.stats import get_subject_averages
    
    averages = get_subject_averages()
    return averages.get(subject, 75)  # Default to 75 if not found

def predict_improvement_needed(student_name, subject, target_score):
    """
    Calculate how much improvement is needed to reach target score.
    """
    student = get_student_by_name(student_name)
    
    if not student:
        return {'error': f'Student {student_name} not found'}
    
    if subject not in student['marks']:
        return {'error': f'No data for {subject}'}
    
    current_score = student['marks'][subject]
    needed = target_score - current_score
    
    if needed <= 0:
        return {
            'message': f'{student_name} has already achieved the target!',
            'current': current_score,
            'target': target_score,
            'status': 'achieved'
        }
    
    # Get predicted next score
    prediction = predict_score(student_name, subject)
    
    if 'error' not in prediction:
        predicted = prediction['predicted_score']
        gap = target_score - predicted
        
        return {
            'current_score': current_score,
            'target_score': target_score,
            'predicted_next': predicted,
            'improvement_needed': round(needed, 2),
            'gap_after_next': round(gap, 2),
            'achievable': 'Yes' if gap <= 5 else 'Needs more effort',
            'message': f'Need to improve by {needed} points. Predicted next: {predicted}'
        }
    
    return {
        'current_score': current_score,
        'target_score': target_score,
        'improvement_needed': round(needed, 2),
        'message': f'Need to improve by {needed} points'
    }

def batch_predict(subject):
    """
    Predict scores for all students in a subject.
    Useful for class-wide analysis.
    """
    from models.student_model import get_all_students
    
    students = get_all_students()
    predictions = []
    
    for student in students:
        if subject in student['marks']:
            result = predict_score(student['name'], subject)
            
            if 'error' not in result:
                predictions.append({
                    'name': student['name'],
                    'current': student['marks'][subject],
                    'predicted': result['predicted_score'],
                    'trend': result.get('trend', 'stable')
                })
    
    return predictions
