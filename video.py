from moviepy import *
import random
import os

def generate_clip(video_id, captions, character, student):

    audio = AudioFileClip(f"media/audio/{video_id}/audio_{video_id}.wav")
    duration_in_seconds = audio.duration


    #BACKGROUND VIDEO
    full_clip = VideoFileClip("media/backgrounds/parkour1.mp4", audio=False)
    clip = full_clip.subclipped(30, 32 + duration_in_seconds)

    clip = clip.resized(height=1920)
    clip = clip.cropped(x1=1166.6,y1=0,x2=2246.6,y2=1920)


    #SPRITES
    teacher_sprite = (ImageClip(character["sprite"]).resized(height=600).with_position((50, 280)))
    student_sprite = (ImageClip(student["sprite"]).resized(height=600).with_position((600, 280)))

    #SPRITE OPACITY
    teacher_dim = teacher_sprite.with_duration(duration_in_seconds).with_opacity(0.3)
    student_dim = student_sprite.with_duration(duration_in_seconds).with_opacity(0.3)

    sprite_clips = [teacher_dim, student_dim]

    for item in captions:

        start = item["start"]
        duration = item["end"] - item["start"]

        if item["colour"] == character["colour"]:
            speaking_sprite = teacher_sprite
        else:
            speaking_sprite = student_sprite

        # Bright copy of the speaking character
        sprite_clips.append(
            speaking_sprite
            .with_start(start)
            .with_duration(duration)
            .with_opacity(1.0)
        )


    #CAPTIONS
    caption_clips = []
    for item in captions:
        caption_length = item["end"] - item["start"]

        txt_clip = (
            TextClip(
                text=item["text"],
                font="arial",
                font_size=50,
                color=item["colour"],
                stroke_color="black",
                stroke_width=5,
                size=(1060, 400),
                horizontal_align="center",
                vertical_align="top",
                method="caption",
            )
            .with_start(item["start"])
            .with_duration(caption_length)
            .with_position(("center", 1450))
        )

        caption_clips.append(txt_clip)

    #background music
    random_choice = random.choice(os.listdir("media/backgrounds/bg_music"))
    bg_music = AudioFileClip(f"media/backgrounds/bg_music/{random_choice}")
    bg_music = bg_music.subclipped(0, duration_in_seconds) #make bg music same length as video
    bg_music = bg_music.with_volume_scaled(0.12) #lower volume

    # Combine dialogue + music
    final_audio = CompositeAudioClip([
        audio,
        bg_music
    ])

    #FINAL VIDEO GENERATION
    video = CompositeVideoClip([clip, *sprite_clips, *caption_clips])
    final_clip = video.with_audio(final_audio)

    final_clip.write_videofile(f"media/completed_videos/testvideo{video_id}.mp4", fps=24, audio_codec="aac")

    return random_choice