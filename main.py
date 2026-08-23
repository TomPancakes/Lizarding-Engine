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
concept = "How microwave ovens work?"  # hardcoded for now

print(f"Using: {character['name']} + {student['name']}")

##
# Generate Script Block
##

preload = input("Do you want to query API or use the preloaded script (yes or no)")
if preload == "yes":
    from generate_script import build_prompt, generate_script
    script_text = generate_script(build_prompt(character, student, concept))
    print(script_text, "\n")   
elif preload == "no":
    script_text = """
STUDENT: Sensei, I dropped my slushie ice in my soda and it floated, which is crazy because I thought heavy frozen stuff should sink like a rock! Like my grades!

TEACHER: Ah! A classic question from a foolish mind! But fear not, for I, your brilliant teacher, shall illuminate this dark abyss of ignorance!

TEACHER: It all comes down to density, my goofy friend. Most things get smaller and tighter when they freeze, right? But water is a weird, stubborn little rebel that completely defies normal logic!

STUDENT: Wait, so water is basically cheating at physics? Does it get fat when it gets cold? Like me during winter break? Haha!

TEACHER: Surprisingly, yes! When water freezes, its molecules form these special hydrogen bonds that push them apart into a spacious, hexagonal cage structure.

TEACHER: Because those molecules are spreading out instead of packing tightly, ice ends up less dense than the liquid water around it. It expands! So the ice floats, saving fish from getting crushed every winter!

STUDENT: Whoa, so ice is basically a tiny, frozen life preserver holding a dance party inside?

TEACHER: Exactly! It refuses to sink no matter how cold and harsh the world gets! It just keeps floating! Honestly, I kind of relate to it.
    """

##
# Generate Audio Block
##

import os
import asyncio
from generate_audio import generate_audio

video_id = len(os.listdir("media/audio"))
os.makedirs(f"media/audio/{video_id}", exist_ok=True)

colour_order = asyncio.run(generate_audio(script_text, character, student, video_id)) #This function actually creates the audio too
print(colour_order) #test this for now

audio_path = f"media/audio/{video_id}/audio_{video_id}.mp3" #get the path of combined audio now created

##
# Generate Captions Block
##
from generate_captions import transcribe

captions = transcribe(audio_path, colour_order) # captions is list of dictionaries. (each with start, end, text keys)

for item in captions[:10]:
    print(f"id: {item['id']}. start: {item['start']:.2f}. end: {item['end']:.2f}. colour: {item['colour']}. text: {item['text'].strip()}")

## so if i want to access these later? i being index (which caption ordered), then the key: text
# captions[i]["text"]


##
# Assemble Video Block
##

from video import generate_clip

generate_clip(video_id, captions)


