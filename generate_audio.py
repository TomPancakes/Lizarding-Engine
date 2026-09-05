import edge_tts
from moviepy import AudioFileClip, concatenate_audioclips
import asyncio
import os


async def generate_audio(script_text, character, student, video_id):

    audio_files = []
    speaker_order = []

    if character['voice']['provider'] == "chatterbox" or student['voice']['provider'] == "chatterbox": #load the nano model IF to be used
        import torchaudio as ta
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        model = ChatterboxTurboTTS.from_pretrained(device="cpu")

    for i, line in enumerate(script_text.splitlines()):

        if line.startswith("TEACHER:"):
            text = line.removeprefix("TEACHER:").strip()
            voice_id = character["voice"]["voice_id"]
            audio_path = f"media/audio/{video_id}/teacher{i}.wav"
            provider = character["voice"]["provider"]
            speaker_order.append({"character_name": character["name"], "role": "teacher", "text": text}) #creates for captions use
        elif line.startswith("STUDENT:"):
            text = line.removeprefix("STUDENT:").strip()
            voice_id = student["voice"]["voice_id"]
            audio_path = f"media/audio/{video_id}/student{i}.wav"
            provider = student["voice"]["provider"]
            speaker_order.append({"character_name": student["name"], "role": "student", "text": text}) #creates for captions use
        else:
            continue #skip anything that doesn't match expected format


        if provider == "edge-tts":
            print(f"Generating Line Numer {i} | with {voice_id}| VIA EDGETTS")
            tts = edge_tts.Communicate(text=text, voice=voice_id)
            await tts.save(audio_path)
            await asyncio.sleep(0.1) # pause to not overload server
        elif provider == "chatterbox":
            print(f"Generating Line Numer {i} | with {voice_id}| VIA CHATTERBOX")
            wav = model.generate(text, audio_prompt_path=voice_id)
            ta.save(audio_path, wav, model.sr)

        audio_files.append(audio_path) #a list of each audio file path. 


    clips = []
    cumulative_time = 0

    # Load each audio file and calculate speaker timings. Add to speaker order. 
    for i, file in enumerate(audio_files):

        clip = AudioFileClip(file)
        clips.append(clip)
        speaker_order[i]["start"] = cumulative_time
        speaker_order[i]["end"] = cumulative_time + clip.duration

        cumulative_time += clip.duration

    # Combine all clips
    combined = concatenate_audioclips(clips)
    combined_path = f"media/audio/{video_id}/audio_{video_id}.wav"
    combined.write_audiofile(combined_path)

    # Close MoviePy clips so Windows releases the WAV files
    combined.close()

    for clip in clips:
        clip.close()

    # Now safely delete individual recordings
    for file in audio_files:
        if os.path.exists(file):
            os.remove(file)

    return speaker_order
