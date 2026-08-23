#####
#Orchestrator File
#####

#import libraries
import json
import random

###
### Topic Selection (EDIT)
###
with open("characters.json", "r") as file:
    characters = json.load(file)

character = random.choice(characters["characters"])
student = random.choice(characters["students"])
concept = "Why metal feels colder than wood?"  # hardcoded for now

print(f"Using: {character['name']} + {student['name']}")

##
# Generate Script Block
##
from generate_script import build_prompt, generate_script

script_text = generate_script(build_prompt(character, student, concept))

print(script_text)

##
# Generate Audio Block
##

import os
import asyncio
from generate_audio import generate_audio

video_id = len(os.listdir("media/audio"))
os.makedirs(f"media/audio/{video_id}", exist_ok=True)

combined_path = asyncio.run(generate_audio(script_text, character, student, video_id)
)

##
# Generate Captions Block
##
from generate_captions import transcribe

captions = transcribe(combined_path) # captions is list of dictionaries. (each with start, end, text keys)
print(captions)


##
# Assemble Video Block
##


