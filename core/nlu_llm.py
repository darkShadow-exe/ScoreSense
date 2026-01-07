import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_command(text):
    """
    Parse natural language command using LLM and extract structured data.
    
    Returns:
        dict with 'intent', 'name', 'marks', 'subject', 'error' keys
    """
    api_key = os.getenv('HACKCLUB_AI_API_KEY')
    base_url = os.getenv('HACKCLUB_AI_BASE_URL', 'https://ai.hackclub.com/proxy/v1')
    model = os.getenv('HACKCLUB_AI_MODEL', 'qwen/qwen3-32b')
    
    if not api_key or api_key == 'your_api_key_here':
        return {
            'intent': 'error',
            'error': 'Please set your HACKCLUB_AI_API_KEY in the .env file'
        }
    
    try:
        # Create structured prompt for the LLM
        system_prompt = """
You are a student management system command parser. Parse natural language commands and return structured JSON.

Supported intents:
- ADD_STUDENT: Add new student profile (name, grade, section, age)
- ADD_EXAM: Add exam scores for existing student
- UPDATE_STUDENT: Update student information
- DELETE_STUDENT: Remove student
- SHOW_TOPPER: Find best performing student
- SHOW_STATS: Show class statistics
- PREDICT: Predict future performance
- GET_RANK: Get student ranking
- COMPARE: Compare students

Response format (JSON only):
{
    "intent": "intent_name",
    "name": "student_name", 
    "marks": {"subject": score}, // for ADD_EXAM
    "grade": "grade_level", // for ADD_STUDENT
    "section": "section_name", // for ADD_STUDENT
    "age": age_number, // for ADD_STUDENT
    "subject": "subject_name", // for PREDICT/COMPARE
    "exam_name": "exam_name", // for ADD_EXAM
    "error": "error_message" // if parsing fails
}

Examples:
"Add student John grade 10 section A" → {"intent": "ADD_STUDENT", "name": "John", "grade": "10", "section": "A"}
"Add exam for Sarah: Math 95, Physics 88" → {"intent": "ADD_EXAM", "name": "Sarah", "marks": {"math": 95, "physics": 88}}
"Who is the topper in math?" → {"intent": "SHOW_TOPPER", "subject": "math"}
"""
        
        # Make API request to Hack Club AI
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': f'Parse this command: "{text}"'}
                ],
                'temperature': 0.1,  # Low temperature for consistent parsing
                'max_tokens': 500
            },
            timeout=30
        )
        
        if response.status_code != 200:
            return {
                'intent': 'error',
                'error': f'API Error: {response.status_code} - {response.text}'
            }
        
        result = response.json()
        llm_response = result['choices'][0]['message']['content'].strip()
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response (might be wrapped in markdown code blocks)
            if '```json' in llm_response:
                json_start = llm_response.find('```json') + 7
                json_end = llm_response.find('```', json_start)
                json_str = llm_response[json_start:json_end].strip()
            elif '{' in llm_response and '}' in llm_response:
                json_start = llm_response.find('{')
                json_end = llm_response.rfind('}') + 1
                json_str = llm_response[json_start:json_end]
            else:
                json_str = llm_response
            
            parsed_command = json.loads(json_str)
            
            # Validate required fields
            if 'intent' not in parsed_command:
                return {
                    'intent': 'error',
                    'error': 'Invalid command format - no intent found'
                }
            
            # Normalize intent to uppercase
            parsed_command['intent'] = parsed_command['intent'].upper()
            
            return parsed_command
            
        except json.JSONDecodeError as e:
            return {
                'intent': 'error',
                'error': f'Failed to parse LLM response as JSON: {str(e)}. Response: {llm_response}'
            }
    
    except requests.exceptions.Timeout:
        return {
            'intent': 'error',
            'error': 'Request timeout - please try again'
        }
    except requests.exceptions.RequestException as e:
        return {
            'intent': 'error',
            'error': f'Network error: {str(e)}'
        }
    except Exception as e:
        return {
            'intent': 'error',
            'error': f'Unexpected error: {str(e)}'
        }