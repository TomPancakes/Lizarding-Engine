import os
from dotenv import load_dotenv

from google import genai

from groq import Groq

load_dotenv()

def build_prompt(character, student, concept):
    return f"""Write a short dialogue script (~90 seconds spoken, 180-230 words)
between a teacher and student explaining: "{concept}".

Aim to be entertaining, informative and easily-comprehensible. Most speaking should be done by the teacher. The student and teacher are familiar with each other.

IMPORTANT OPENING:
The first few lines must immediately establish the context for a viewer who has just started watching.
Either the teacher introduces you themselves in a natural way, or the student asks them something with their name.
After establishing the context, transition into an interesting hook, joke, analogy, or surprising fact.
Do NOT begin with an analogy, joke, or explanation that assumes the viewer already knows what the topic is.

Do not copy this example literally. Make the dialogue natural to the characters.

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

Multiple teacher or student lines in a row are allowed when natural.

No stage directions, no markdown, just the dialogue.
"""


def generate_script(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text


