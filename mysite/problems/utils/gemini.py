import google.generativeai as genai
import os

# Set your Gemini API Key securely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set in .env or your server config
genai.configure(api_key="GEMINI_API_KEY")

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

def review_code(code: str, language: str, verdict: str, problem_title: str, problem_statement: str) -> str:
    prompt = f"""You're an expert coding assistant and reviewer.

The user attempted to solve the following problem:

### Problem Title:
{problem_title}

### Problem Statement:
{problem_statement}

---

### Submission Details:
- Language: {language}
- Execution Result: {verdict}

### Code:
{code}

---

Please provide a constructive code review in a very concise way that covers:
1. Suggestions for improvement if any or if the code is wrong tell the user where is the mistake

Keep the tone friendly and clear for a student-level developer.
Dont give any code snippet or code in the response.
It has to be only a suggestion without any code snippet.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Review Failed: {e}"
