from moviepy import *

def generate_clip(video_id, captions):

    audio = AudioFileClip(f"media/audio/{video_id}/audio_{video_id}.mp3")
    duration_in_seconds = audio.duration

    clip = (VideoFileClip("media/backgrounds/parkour1.mp4")
    .subclipped(30, 32 + duration_in_seconds)
    .resized(height=1920)
    .cropped(x_center=960, width=1080, height=1920)
    .with_fps(24))


    caption_clips = []
    for item in captions:
        caption_length = item["end"] - item["start"]

        txt_clip = (TextClip(text=item["text"], font="arial.ttf", font_size=50, color=item["colour"], size=(1000, None), method="caption")
                    .with_start(item["start"])
                    .with_duration(caption_length)
                    .with_position("center"))

        caption_clips.append(txt_clip)

    video = CompositeVideoClip([clip, *caption_clips])
    final_clip = video.with_audio(audio)

    final_clip.write_videofile(f"media/completed_videos/testvideo{video_id}.mp4", fps=24, audio_codec="aac")
