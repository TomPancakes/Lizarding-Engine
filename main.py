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
with open("topics.json", "r") as file:
    topics = json.load(file)

character = random.choice(characters["characters"])
student = random.choice(characters["students"])
concept = random.choice(topics["topics"])["topic"]
#concept = "Why Dogs are better than Cats"  # Uncomment if want to hard-code topic

print(f"Using: {character['name']} + {student['name']} on {concept}")

##
# Generate Script Block
##

preload = input("Do you want to run in test settings (yes for yes, else enter): ")
if preload == "yes":
    script_text = """
STUDENT: Sensei, I dropped my slushie ice in my soda and it floated, which is crazy because I thought heavy frozen stuff should sink like a rock! Like my grades!

TEACHER: Ah! A classic question from a foolish mind! But fear not, for I, your brilliant teacher, shall illuminate this dark abyss of ignorance!

TEACHER: It all comes down to density, my goofy friend. Most things get smaller and tighter when they freeze, right? But water is a weird, stubborn little rebel that completely defies normal logic!

STUDENT: Wait, so water is basically cheating at physics? Does it get fat when it gets cold? Like me during winter break? Haha!
    """
else:
    from generate_script import build_prompt, generate_script
    script_text = generate_script(build_prompt(character, student, concept))
    print(script_text, "\n")  

##
# Generate Audio Block
##

import os
import asyncio
from generate_audio import generate_audio

video_id = len(os.listdir("media/audio"))
os.makedirs(f"media/audio/{video_id}", exist_ok=True)

speaking_order = asyncio.run(generate_audio(script_text, character, student, video_id)) #This function actually creates the audio too

audio_path = f"media/audio/{video_id}/audio_{video_id}.wav" #get the path of combined audio now created

##
# Generate Captions Block
##

from updated_captions import generate_captions

caption_length = 8

captions = generate_captions(speaking_order, character, student, caption_length)
for item in captions[:10]:
    print(item)


#from generate_captions import transcribe

#captions = transcribe(audio_path, colour_order) # captions is list of dictionaries. (each with start, end, text keys)

#for item in captions[:10]:
#    print(f"id: {item['id']}. start: {item['start']:.2f}. end: {item['end']:.2f}. colour: {item['colour']}. text: {item['text'].strip()}")

## so if i want to access these later? i being index (which caption ordered), then the key: text
# captions[i]["text"]


##
# Assemble Video Block
##

from video import generate_clip

music_choice = generate_clip(video_id, captions, character, student) #CREATES THE VIDEO! (also returns what bg song is used)
final_video = f"media/completed_videos/testvideo{video_id}.mp4"
print(f"Succsesfully Generated Video at {final_video}. Character: {character['name']}. Student: {student['name']}. Topic: {concept}")
print(f"music choice: {music_choice}")

## upload video block
