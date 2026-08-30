import edge_tts
from moviepy import AudioFileClip, concatenate_audioclips
import asyncio
import os

import subprocess
import json
import tempfile

CB_PYTHON = r"C:/Users/Tom\Desktop/Code Projects/Lizarding Engine/.venv_cb\Scripts/python.exe"
CB_WORKER = r"C:/Users/Tom\Desktop/Code Projects/Lizarding Engine/chatterbox_worker.py"

def run_chatterbox_batch(jobs):
    """jobs = [{"text": ..., "output_path": ..., "voice_id": ...}, ...]"""
    if not jobs:
        return
 
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(jobs, f)
        jobs_path = f.name
 
    print(f"Sending {len(jobs)} lines to Chatterbox subprocess...")
    subprocess.run([CB_PYTHON, CB_WORKER, jobs_path], check=True)
    os.remove(jobs_path)


async def generate_audio(script_text, character, student, video_id):

    audio_files = []
    speaker_order = []
    chatterbox_jobs = []

    for i, line in enumerate(script_text.splitlines()):

        if line.startswith("TEACHER:"):
            text = line.removeprefix("TEACHER:").strip()
            voice_id = character["voice"]["voice_id"]
            audio_path = f"media/audio/{video_id}/teacher{i}.wav"
            text_colour = character["colour"]
            provider = character["voice"]["provider"]
        elif line.startswith("STUDENT:"):
            text = line.removeprefix("STUDENT:").strip()
            voice_id = student["voice"]["voice_id"]
            audio_path = f"media/audio/{video_id}/student{i}.wav"
            text_colour = student["colour"]
            provider = student["voice"]["provider"]
        else:
            continue #skip anything that doesn't match expected format


        if provider == "edge-tts":
            print(f"Generating Line Numer {i} | with {voice_id}| VIA EDGETTS")
            tts = edge_tts.Communicate(text=text, voice=voice_id)
            await tts.save(audio_path)
            await asyncio.sleep(0.1) # pause to not overload server
        elif provider == "chatterbox":
            # don't generate now - queue it up for the batch subprocess call below
            chatterbox_jobs.append({
                "text": text,
                "output_path": audio_path,
                "voice_id": voice_id
            })

        speaker_order.append({"colour": text_colour}) # speaker order looks like this ["green","green","blue","green","blue","green",]
        audio_files.append(audio_path) #a list of each audio file path. 

    run_chatterbox_batch(chatterbox_jobs) #generate all queued chatterbox lines

    clips = []
    cumulative_time = 0

    # Load each audio file and calculate speaker timings
    for i, file in enumerate(audio_files):

        clip = AudioFileClip(file)
        clips.append(clip)
        speaker_order[i]["time"] = cumulative_time
        cumulative_time += clip.duration

    # Combine all clips
    combined = concatenate_audioclips(clips)
    combined_path = f"media/audio/{video_id}/audio_{video_id}.wav"
    combined.write_audiofile(combined_path)

    # IMPORTANT: Close MoviePy clips so Windows releases the WAV files
    combined.close()

    for clip in clips:
        clip.close()

    # Now safely delete individual recordings
    for file in audio_files:
        if os.path.exists(file):
            os.remove(file)

    return speaker_order
