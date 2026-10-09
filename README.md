# Complete YouTube Shorts Content Pipeline 

## Overview
A Python pipeline that generates educational YouTube Shorts end to end, in the format **Character X explains Topic Y to Character Z**.

Channel example: [Lizarding Academy](https://www.youtube.com/@LizardingAcademy)

## How it works?
Different files are responsible for different parts of the pipeline. x.py Acts as the orchestrator file, which includes the main loop, and calls each function 

### Files Responsible for Generating parts of a video: (runs in the following order) 
- **generate_script:** Generates script, using Google Gemini API. Prompt is built with selected character (and associated traits) & topic selected
- **generate_audio:** Generates audio using locally run chatterbox
- **updated_captions:** Generates captions based on 8 word per caption length. Caption colour is assigned using audio snippet timestamps
- **video.py:** Video assembly file. Uses MoviePy to splice all media (audio, captions, background footage, character models) and generates final mp4 output
- **upload.py** Publishes final video to Youtube via Youtube Data API v3


## How to run
The pipeline needs two config files and a `media/` folder before it will run. Neither is included in the repo (personal characters and images are gitignored), so you'll need to create your own.

### 1. Config files
Create both in the project root.

#### `topics.json`
Stores every topic the pipeline can make a video about. `done` tracks whether a video has already been made for that topic.

```json
{
  "topics": [
    { "topic": "Why is the sky blue", "done": false },
    { "topic": "How do magnets work", "done": false }
  ]
}
```

#### `characters.json`
Has two lists: `characters` (the teachers) and `students`. Both use the same fields.

```json
{
  "characters": [
    {
      "name": "Professor Example",
      "gender": "male",
      "source": "Example Series",
      "personality": "Calm, patient, loves a good analogy",
      "relationships": "Sam: his student and favourite person to explain things to",
      "speech_style": "Warm and clear, with the occasional dry joke",
      "lore/abilities": "Background info, abilities or running jokes the script can draw on",
      "voice": {
        "provider": "chatterbox",
        "voice_id": "media/character_models/character.wavs/professor_snippet.mp3"
      },
      "sprite": "media/character_models/professor_model.png",
      "colour": "white"
    }
  ],
  "students": [
    {
      "name": "Sam",
      "gender": "female",
      "source": "N/A",
      "personality": "Curious, asks a lot of questions",
      "relationships": "Professor Example: her teacher",
      "speech_style": "Quick and enthusiastic",
      "lore/abilities": "N/A",
      "voice": {
        "provider": "chatterbox",
        "voice_id": "media/character_models/character.wavs/sam_snippet.mp3"
      },
      "sprite": "media/character_models/sam_model.png",
      "colour": "cornflowerblue"
    }
  ]
}
```

| Field | What it does |
|---|---|
| `name` | Character's name, used in the script, video title and description |
| `gender` | Character's gender, used when building the script prompt |
| `source` | Where the character is from (`N/A` for original characters) |
| `personality`, `relationships`, `speech_style`, `lore/abilities` | Fed into the Gemini prompt so the script matches the character |
| `voice.provider` | TTS engine (currently `chatterbox`) |
| `voice.voice_id` | Path to a short audio clip of the character, used for voice cloning |
| `sprite` | Path to the character's image (PNG with a transparent background works best) |
| `colour` | Caption colour for this character's lines (any CSS colour name, e.g. `white`, `mediumpurple`) |

### 2. Media folder
Create this structure in the project root:

```
media/
├── audio/                  # Generated TTS audio (written by the pipeline)
├── background_footage/     # Background video clips (.mp4)
├── bg_music/               # Background music (.mp3)
├── character_models/       # Character sprites (.png, transparent background)
│   └── character.wavs/     # Short voice clips used for TTS cloning
└── completed_videos/       # Final rendered videos
```

Paths in `characters.json` are relative to the project root, so a sprite at `media/character_models/professor_model.png` is referenced exactly like that.

### Dependencies
- Python 3.11

```bash
pip install chatterbox-tts moviepy google-genai google-api-python-client google-auth-oauthlib python-dotenv
```