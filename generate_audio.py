import edge_tts
import torchaudio as ta
import torch
from chatterbox.tts_turbo import ChatterboxTurboTTS
from moviepy import AudioFileClip, concatenate_audioclips
import asyncio
import os



async def generate_audio(script_text, character, student, video_id):

    model = ChatterboxTurboTTS.from_pretrained(device="cuda")

    audio_files = []
    speaker_order = []

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

        print(f"Generating: voice={voice_id} | Audio Line Number: {i}")
        if provider == "chatterbox":
            wav = model.generate(text, audio_prompt_path=voice_id)
            ta.save(audio_path, wav, model.sr)
        elif provider == "edge-tts":
            tts = edge_tts.Communicate(text=text, voice=voice_id)
            await tts.save(audio_path)
            await asyncio.sleep(0.1) # pause to not overload server

        speaker_order.append({"colour": text_colour})
        audio_files.append(audio_path)


    # speaker order looks like this ["green","green","blue","green","blue","green",]

    clips = []
    cumulative_time = 0
    i = 0

    for file in audio_files: #assigns speaker order with colour AND 
        clips.append(AudioFileClip(file))
        speaker_order[i]["time"] = cumulative_time #add entry for cumulative time
        cumulative_time += AudioFileClip(file).duration
        i += 1


    combined = concatenate_audioclips(clips)

    combined_path = f"media/audio/{video_id}/audio_{video_id}.wav"
    combined.write_audiofile(combined_path)

    for file in audio_files: #remove all now unneeded invidiaul recordings leaving only combined
        filename = os.path.basename(file)
        if filename.startswith("student") or filename.startswith("teacher"):
            os.remove(file)

    return speaker_order
