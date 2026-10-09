#this simplified version of the captions will break the raw script into approximate chunks
#rather than using whisper which generates captions too large for short form content

#speaking order: precise start and end time for each character. 

def generate_captions(speaking_order, character, student, max_length):

    caption_list = []

    for line in speaking_order:
        colour = student["colour"] if line["role"] == "student" else character["colour"]

        words = line["text"].split()
        duration = line["end"] - line["start"]
        seconds_per_word = duration / len(words)

        chunk_start = line["start"]

        for i in range(0, len(words), max_length):
            chunk_words = words[i:i + max_length]
            chunk_end = chunk_start + (len(chunk_words) * seconds_per_word)

            caption_list.append({
                "text": " ".join(chunk_words),
                "character_name": line["character_name"],
                "role": line["role"],
                "colour": colour,
                "start": chunk_start,
                "end": chunk_end,
            })

            chunk_start = chunk_end

    return caption_list


#{'character': 'Sara', 'role': 'student', 'text': 'Sensei, I dropped my slushie ice in my soda and it floated, which is crazy because I thought heavy frozen stuff should sink like a rock! Like my grades!', 'start': 0, 'end': 10.08}