import google.generativeai as genai
from django.conf import settings

def generate_content(prompt):
    """
    Uses the Gemini API to generate text content.
    :param prompt: Text prompt for the API.
    :return: Generated content.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"
    
    
    
def generate_text(prompt):
    """
    Uses the Gemini API to generate text content.
    :param prompt: Text prompt for the API.
    :return: Generated content.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"