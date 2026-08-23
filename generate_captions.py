import whisper 
import os

def transcribe(mp3): 

    model = whisper.load_model("base")

    result = model.transcribe(mp3)

    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        print(f"[{start:.2f}s - {end:.2f}s] {text}")

    return result["segments"]
