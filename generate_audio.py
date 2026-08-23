import edge_tts
from moviepy import AudioFileClip, concatenate_audioclips
import asyncio

async def generate_audio(script_text, character, student, video_id):

    audio_files = []

    for i, line in enumerate(script_text.splitlines()):

        if line.startswith("TEACHER:"):
            text = line.removeprefix("TEACHER:").strip()
            voice_id = character["voice"]["voice_id"]
            audio_path = f"media/audio/{video_id}/teacher{i}.mp3"

        elif line.startswith("STUDENT:"):
            text = line.removeprefix("STUDENT:").strip()
            voice_id = student["voice"]["voice_id"]
            audio_path = f"media/audio/{video_id}/student{i}.mp3"

        else:
            continue #skip anything that doesn't match expected format

        print(f"Generating: voice={voice_id} | text={text!r}")
        tts = edge_tts.Communicate(text=text, voice=voice_id)
        await tts.save(audio_path)

        await asyncio.sleep(0.1) # pause to not overload server

        audio_files.append(audio_path)

    clips = []

    for file in audio_files:
        clips.append(AudioFileClip(file))

    combined = concatenate_audioclips(clips)

    combined_path = f"media/audio/{video_id}/audio_{video_id}.mp3"
    combined.write_audiofile(combined_path)

    return combined_path

