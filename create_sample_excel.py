"""
Create sample Excel files for testing the import feature.
"""

import pandas as pd
import random

# Sample 1: Wide format with exam names
data1 = {
    'Student Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Adams'],
    'Exam': ['Midterm', 'Midterm', 'Midterm', 'Midterm', 'Midterm'],
    'Mathematics': [92, 78, 88, 95, 82],
    'Physics': [88, 82, 90, 91, 85],
    'Chemistry': [85, 79, 87, 93, 88],
    'Biology': [90, 84, 89, 96, 86],
    'English': [87, 81, 91, 89, 83]
}

df1 = pd.DataFrame(data1)
df1.to_excel('sample_imports/sample_wide_format.xlsx', index=False)
print("✓ Created sample_wide_format.xlsx")

# Sample 2: Simple format without exam names
data2 = {
    'Name': ['Frank Miller', 'Grace Lee', 'Henry Davis', 'Iris Chen', 'Jack Wilson'],
    'Math': [85, 92, 79, 88, 91],
    'Science': [88, 89, 83, 90, 87],
    'English': [82, 94, 78, 85, 89],
    'History': [86, 90, 81, 87, 88]
}

df2 = pd.DataFrame(data2)
df2.to_excel('sample_imports/sample_simple_format.xlsx', index=False)
print("✓ Created sample_simple_format.xlsx")

# Sample 3: Different structure with full names
data3 = {
    'Pupil': ['Katherine Green', 'Leo Martinez', 'Maya Patel', 'Noah Anderson'],
    'Test Name': ['Finals', 'Finals', 'Finals', 'Finals'],
    'Computer Science': [94, 87, 91, 89],
    'Mathematics': [89, 92, 88, 93],
    'Physics': [91, 85, 94, 90],
    'Chemistry': [87, 89, 92, 91]
}

df3 = pd.DataFrame(data3)
df3.to_excel('sample_imports/sample_different_structure.xlsx', index=False)
print("✓ Created sample_different_structure.xlsx")

print("\n✅ Sample Excel files created in 'sample_imports/' directory")
print("You can use these files to test the import feature!")
