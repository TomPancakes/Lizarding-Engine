import os
from dotenv import load_dotenv

from google import genai

load_dotenv()


def build_prompt(character, student, concept, variant):
    if variant == "original":
        return f"""Write an entertaining, informative, easily comprehensible dialogue script
between a teacher and student explaining: "{concept}".

Spoken length should be 30 to 60 seconds (roughly 90 to 220 words).
Decide the length based on what this concept and character dynamic actually need — don't pad
to hit a target. Only use the extra time if you judge it is genuinely needed or adds value. 

Focus on ONE central idea — don't try to cover the whole topic.
Don't force strict back-and-forth alternation — sometimes it's more natural for the
teacher or student to speak for multiple lines in a row.

TEACHER: {character['name']}
Gender: {character['gender']}
Personality: {character['personality']}
Speech style: {character['speech_style']}
Lore/abilities: {character['lore/abilities']}
Canonical Relationships: {character['relationships']}

STUDENT: {student['name']}
Gender: {student['gender']}
Personality: {student['personality']}
Speech style: {student['speech_style']}
Lore/abilities: {student['lore/abilities']}
Canonical Relationships: {student['relationships']}

Format each line as:
TEACHER: <line>
or
STUDENT: <line>

OPENING LINE: Begin with a hook, or line which clearly states the topic being discussed in a way natural to {student['name']}

No stage directions, no markdown, just the dialogue.
""", variant

    return f"""Write an entertaining, informative, easily comprehensible dialogue script
(between a teacher and student explaining: "{concept}".

Spoken length should be 30 to 60 seconds (roughly 90 to 220 words).
Decide the length based on what this concept and character dynamic actually need — don't pad
to hit a target. Only use the extra time if you judge it is genuinely needed or adds value. 

Focus on ONE central idea — don't try to cover the whole topic.
Don't force strict back-and-forth alternation — sometimes it's more natural for the
teacher or student to speak for multiple lines in a row.

TEACHER: {character['name']}
Gender: {character['gender']}
Personality: {character['personality']}
Speech style: {character['speech_style']}
Lore/abilities: {character['lore/abilities']}
Canonical Relationships: {character['relationships']}

STUDENT: {student['name']}
Gender: {student['gender']}
Personality: {student['personality']}
Speech style: {student['speech_style']}
Lore/abilities: {student['lore/abilities']}
Canonical Relationships: {student['relationships']}

OPENING LINE: This is the single most important line in the script — viewers decide
whether to keep watching within the first 2-3 seconds, so it must hook immediately
AND be instantly understandable. Clever but confusing is just as bad as boring —
both get swiped away. A viewer who has never seen this character before should
immediately grasp WHO is talking, WHAT is happening, and WHY they should care,
even if they don't yet know the specific topic.
Either {character['name']} or {student['name']} can speak first, whichever is more
in-character for a strong opener.
Pick ONE hook mechanism (don't just announce the topic):
- A surprising or seemingly-false claim that turns out to be true
- Dropping in mid-argument or mid-reaction, as if we caught the middle of a moment
  already in progress
- A callout or dare aimed at the other character, in their voice
- A question that reframes something ordinary as strange or broken
Keep the language simple and concrete, not abstract or riddle-like. No inside jokes,
no lines that only make sense in hindsight, no vague pronouns with unclear referents
("it," "that," "this") in the very first line. The hook should create curiosity about
WHERE THIS IS GOING, not confusion about WHAT IS BEING SAID.
The opening line must sound like it could ONLY come from that character — use their
specific personality, speech style, and lore, not generic phrasing. Never open with
"What is X?", "Can you explain X?", "Today we're learning about X," or any line that
just names or previews the topic.

Format each line as:
TEACHER: <line>
or
STUDENT: <line>

No stage directions, no markdown, just the dialogue.
""", variant


def generate_script(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

