import os
from dotenv import load_dotenv

from google import genai

from groq import Groq

load_dotenv()

def build_prompt(character, student, concept):
    return f"""Write a short dialogue script (~90 seconds spoken, 180-230 words)
between a teacher and student explaining: "{concept}". 
Aim to be entertaining and informative. Most speaking should be done by the teacher. 

TEACHER: {character['name']}
Personality: {character['personality']}
Speech style: {character['speech_style']}

STUDENT: {student['name']}
Personality: {student['personality']}
Speech style: {student['speech_style']}

Format each line as: 
TEACHER: <line>
or
STUDENT: <line>

Note that lines do teacher/student lines do not have to be in order. (Multiple teacher lines in a row is okay if necessary)

No stage directions, no markdown, just the dialogue. 
"""


def generate_script(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text


