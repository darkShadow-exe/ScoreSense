"""Statistical utility functions for score analysis."""

def calculate_stats(scores):
    """Calculate basic statistics for a list of scores."""
    if not scores:
        return {
            'average': 0,
            'highest': 0,
            'lowest': 0,
            'count': 0
        }
    
    return {
        'average': sum(scores) / len(scores),
        'highest': max(scores),
        'lowest': min(scores),
        'count': len(scores)
    }

def get_trend(scores):
    """
    Determine the trend of scores over time.
    Returns: 'improving', 'declining', or 'stable'
    """
    if not scores or len(scores) < 2:
        return 'stable'
    
    # Compare first half average to second half average
    mid = len(scores) // 2
    if mid == 0:
        return 'stable'
    
    first_half_avg = sum(scores[:mid]) / mid
    second_half_avg = sum(scores[mid:]) / (len(scores) - mid)
    
    # 5% threshold for determining trend
    diff_percent = abs(second_half_avg - first_half_avg) / first_half_avg * 100 if first_half_avg > 0 else 0
    
    if diff_percent < 5:
        return 'stable'
    elif second_half_avg > first_half_avg:
        return 'improving'
    else:
        return 'declining'

def calculate_percentile(score, all_scores):
    """Calculate the percentile rank of a score."""
    if not all_scores:
        return 0
    
    below = sum(1 for s in all_scores if s < score)
    return (below / len(all_scores)) * 100

def get_grade_letter(score):
    """Convert numerical score to letter grade."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
