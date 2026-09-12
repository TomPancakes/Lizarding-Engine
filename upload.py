import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secrets.json"  # update if you named it differently
TOKEN_FILE = "token.pickle"


def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


def upload_video(video_path, character, student, concept, music_choice, prompt_choice):
    youtube = get_authenticated_service()

    song_name = music_choice.removesuffix(".mp3").removesuffix(".mp4").removesuffix(".wav")

    title = f"{character['name']} Explains {concept}"
    description = (
        f"{character['name']} explains {concept} to {student['name']}.\n\n"
        f"AI-generated voices used for character dialogue.\n"
        f"AI-generation used to produce script.\n"
        f"song used: {song_name} (NCS) \n"
        f"{prompt_choice}"
    )
    tags = [concept, character['name']]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "1",  # Education
        },
        "status": {
            "privacyStatus": "private",  # flip to "public" once you trust the pipeline
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"Upload complete: https://youtube.com/watch?v={video_id}")

    return video_id


if __name__ == "__main__":
    # quick manual test
    upload_video(
        video_path="final_video.mp4",
        character={"name": "Test Teacher"},
        student={"name": "Test Student"},
        concept="Test Concept",
    )