from moviepy import *

def generate_clip(video_id, captions, character, student):

    audio = AudioFileClip(f"media/audio/{video_id}/audio_{video_id}.mp3")
    duration_in_seconds = audio.duration


    #BACKGROUND VIDEO
    full_clip = VideoFileClip("media/backgrounds/parkour1.mp4", audio=False)
    clip = full_clip.subclipped(30, 32 + duration_in_seconds)

    clip = clip.resized(height=1920)
    clip = clip.cropped(x1=1166.6,y1=0,x2=2246.6,y2=1920)


    # SPRITES

    teacher_sprite = (
        ImageClip(character["sprite"])
        .resized(height=900)
        .with_position((50, 1020))
    )

    student_sprite = (
        ImageClip(student["sprite"])
        .resized(height=900)
        .with_position((600, 1020))
    )

    # SPRITE OPACITY

    sprite_clips = []

    for item in captions:

        start = item["start"]
        duration = item["end"] - item["start"]

        # Caption colour tells us who's talking
        if item["colour"] == character["colour"]:
            speaking_sprite = teacher_sprite
            silent_sprite = student_sprite

        else:
            speaking_sprite = student_sprite
            silent_sprite = teacher_sprite


        # Speaking character
        sprite_clips.append(
            speaking_sprite
            .with_start(start)
            .with_duration(duration)
            .with_opacity(1.0)
        )


        # Non-speaking character
        sprite_clips.append(
            silent_sprite
            .with_start(start)
            .with_duration(duration)
            .with_opacity(0.3)
        )


    #CAPTIONS
    caption_clips = []
    for item in captions:
        caption_length = item["end"] - item["start"]

        txt_clip = (TextClip(text=item["text"], font="arial", font_size=80, color=item["colour"], size=(800, None), method="caption", horizontal_align="center", vertical_align="bottom")
                    .with_start(item["start"])
                    .with_duration(caption_length))

        caption_clips.append(txt_clip)



    #FINAL VIDEO GENERATION

    video = CompositeVideoClip([clip, *sprite_clips, *caption_clips])
    final_clip = video.with_audio(audio)

    final_clip = final_clip.subclipped(0, 15) #THIS LINE TO SHORTEN TIME FOR TESTING. DELETE 

    final_clip.write_videofile(f"media/completed_videos/testvideo{video_id}.mp4", fps=24, audio_codec="aac")

