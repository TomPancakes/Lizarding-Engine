#####
# Orchestrator File
#####

import json
import random
import os
import asyncio
import time
from datetime import datetime

def log_video(video_id, character, student, concept, variant, script_text):
    with open("video_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{'='*40}\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Character: {character['name']}\n")
        f.write(f"Student: {student['name']}\n")
        f.write(f"Concept: {concept}\n")
        f.write(f"Variant: {variant}\n")
        f.write(f"Script:\n{script_text}\n")
        f.write(f"{'='*40}\n\n")


def generation_pipeline(character, student, concept, video_id):
    from generate_script import build_prompt, generate_script
    from generate_audio import generate_audio
    from updated_captions import generate_captions
    from video import generate_clip
    from upload import upload_video

    ########### generate script ###########
    variant = random.choice(["original", "hook_v2"])
    prompt, prompt_choice = build_prompt(character, student, concept, variant)
    script_text = None
    tries = 0
    time_increment = 0
    while tries < 7:
        try:
            script_text = generate_script(prompt)
            break
        except Exception:
            print("Model busy, retrying...")
            tries += 1
            time.sleep(10+time_increment)
            time_increment += 5

    if script_text == None:
        print(f"Script generation failed after retries for video {video_id} on {concept}\n")
        return None, False, True #final_video, upload_limit_hit, script_gen_failed

    ########### generate audio ###########
    os.makedirs(f"media/audio/{video_id}", exist_ok=True)
    speaking_order = asyncio.run(generate_audio(script_text, character, student, video_id)) #This function actually creates the audio too
    audio_path = f"media/audio/{video_id}/audio_{video_id}.wav" #get the path of combined audio now created

    ########### generate captions ###########
    caption_length = 8
    captions = generate_captions(speaking_order, character, student, caption_length)

    #assemble video
    music_choice = generate_clip(video_id, captions, character, student) #CREATES THE VIDEO! (also returns what bg song is used)
    final_video = f"media/completed_videos/testvideo{video_id}.mp4"
    print(f"Succsesfully Generated Video at {final_video}. Character: {character['name']}. Student: {student['name']}. Topic: {concept}")
    print(f"music choice: {music_choice}")

    #upload video to yt (can comment this out if you don't want to upload just generate locally)
    upload_limit_hit = False
    try:
        upload_video(final_video, character, student, concept, music_choice, prompt_choice)
    except Exception as e:
        if "uploadLimitExceeded" in str(e):
            print("Upload limit hit — this video saved locally only.")
            upload_limit_hit = True
        else:
            print(f"Upload failed for other reason: {e}")

    #log video for records sake (useful to analyse prompt variant to script generation)
    log_video(video_id, character, student, concept, variant, script_text)

    os.remove(audio_path)

    return final_video, upload_limit_hit, False


with open("characters.json", "r") as file:
    characters = json.load(file)
with open("topics.json", "r") as file:
    topics = json.load(file)

gen_method = input("Generate in Manual or Auto Mode \nManual (1 at a time. Select fields) \nAuto (multiple at a time randomised fields)\n Enter: ").lower()
if gen_method == "auto":
    num_videos = int(input("How many videos do you want to generate? "))
    locations_video = []
    base_id = len(os.listdir("media/completed_videos")) #so we add i onto this each loop

    start_time = time.time() #to track how long generation took

    for i in range(0, num_videos):
        video_id = base_id + i
        character = random.choice(characters["characters"])
        student = random.choice(characters["students"])
        available_topics = [t for t in topics["topics"] if not t.get("done")]
        if not available_topics:
            print(f"No more undone topics available. Stopping after {i} videos.")
            break
        topic_entry = random.choice(available_topics)
        concept = topic_entry["topic"]
        video, upload_limit_hit, script_gen_failed = generation_pipeline(character, student, concept, video_id) #generates video

        if script_gen_failed:
            print("Script generation is failing repeatedly - stopping batch.")
            break

        locations_video.append(video)
        print(f"Successfully generated video {i} on {concept}")

        topic_entry["done"] = True
        with open("topics.json", "w") as file:
            json.dump(topics, file, separators=(",", ": "), ensure_ascii=False)

        if upload_limit_hit == True:
            print("upload limit hit")
            break

    elapsed = time.time() - start_time
    print(f"Generated {len(locations_video)} videos successfully at {locations_video}. \n Generation Took {elapsed / 60:.1f} minutes")

elif gen_method == "manual":

    video_type = input("What video type would you like to generate (Teacher, debate, )")

    teacher_names = [c["name"] for c in characters["characters"]]
    student_names = [s["name"] for s in characters["students"]]
    print(f"Available teachers: {', '.join(teacher_names)}")
    character_name = input("Please select a character as teacher role (case sensitive): ")

    print(f"Available students: {', '.join(student_names)}")
    student_name = input("Please select a character as student role (case sensitive): ")

    # look up the actual dicts by name
    character = next((c for c in characters["characters"] if c["name"] == character_name), None)
    student = next((s for s in characters["students"] if s["name"] == student_name), None)

    if character is None or student is None:
        print("Name not recognized — check spelling/capitalization. Exiting.")
        exit(1)

    concept = input("Please Enter Desired Topic: \nKeep in mind a stupid topic will probably result in an equally stupid video :) ")
    video_id = len(os.listdir("media/completed_videos"))

    generation_pipeline(character, student, concept, video_id)

