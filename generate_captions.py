import whisper 

def transcribe(mp3, speaker_order): 

    model = whisper.load_model("base")

    result = model.transcribe(mp3)

    cumulative_time_value = 0
    cur_speaker = 0

    for segment in result["segments"]: #iterate through each caption created and add some vars we will need. 
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        #FIND OUT WHICH SPEAKER THIS TIME RANGE BELONGS TO (to determine colour)
        while (cur_speaker + 1 < len(speaker_order)
               and start >= speaker_order[cur_speaker + 1]["time"] - 0.5):
            cur_speaker += 1

        segment["colour"] = speaker_order[cur_speaker]["colour"]

    return result["segments"]


# speaker_order = [
#     {"colour": "green", "time": 0},
#     {"colour": "blue", "time": 5},
#     {"colour": "pink", "time": 8},
# ]