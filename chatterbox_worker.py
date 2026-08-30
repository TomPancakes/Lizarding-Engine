import sys
import json
import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS


def generate_chatterbox_audio(model, text, voice_id, output_path):
    """
    Generates one line of audio using Chatterbox Nano.

    text: the line to speak
    voice_id: path to the reference wav/mp3 for voice cloning
    output_path: where to save the generated audio (already includes video_id)
    """
    wav = model.generate(text, audio_prompt_path=voice_id)
    ta.save(output_path, wav, model.sr)


def main():
    jobs_path = sys.argv[1]
    with open(jobs_path, "r") as f:
        jobs = json.load(f)

    print(f"Loading Chatterbox Nano model ({len(jobs)} lines to generate)...")
    model = ChatterboxTurboTTS.from_pretrained(device="cpu", nano=True)
    print("Model loaded.")

    for job in jobs:
        print(f"Generating: {job['output_path']}")
        generate_chatterbox_audio(
            model=model,
            text=job["text"],
            voice_id=job["voice_id"],
            output_path=job["output_path"]
        )

    print("All chatterbox lines done.")


if __name__ == "__main__":
    main()