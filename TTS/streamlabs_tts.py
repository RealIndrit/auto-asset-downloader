from pathlib import Path
import random
import re
import requests

from requests.exceptions import JSONDecodeError
from tts.tts_helper import check_ratelimit, concatenate_audio_segments, sanitize_text
"""
Credits: https://github.com/elebumm/RedditVideoMakerBot/blob/master/TTS/streamlabs_polly.py
"""
voices = [
    "Brian",
    "Emma",
    "Russell",
    "Joey",
    "Matthew",
    "Joanna",
    "Kimberly",
    "Amy",
    "Geraint",
    "Nicole",
    "Justin",
    "Ivy",
    "Kendra",
    "Salli",
    "Raveena",
]

# Valid voices https://lazypy.ro/tts/


# Part Credits https://github.com/elebumm/RedditVideoMakerBot/blob/master/TTS/streamlabs_polly.py
class StreamlabsPolly:

    def __init__(self):
        self.url = "https://streamlabs.com/polly/speak"
        self.max_chars = 500
        self.voices = voices

    def run(self, text: str, path: str, voice: str):
        if voice.upper == "RANDOM":
            voice = self.randomvoice()
        text = sanitize_text(text)

        if len(text) > self.max_chars:
            self.__split_tts(path, text, voice)
        else:
            self.__call_tts(path, text, voice)

    def randomvoice(self):
        return random.choice(self.voices)

    def __call_tts(self, path: str, text: str, voice: str):
        body = {"voice": voice, "text": text, "service": "polly"}
        response = requests.post(self.url, data=body)
        if not check_ratelimit(response):
            self.run(text, path, voice)
        try:
            voice_data = requests.get(response.json()["speak_url"])
            with open(path, "wb") as f:
                f.write(voice_data.content)
        except (KeyError, JSONDecodeError):
            try:
                if response.json()["error"] == "No text specified!":
                    raise ValueError(
                        "Please specify a text to convert to speech.")
            except (KeyError, JSONDecodeError):
                print("Error occurred calling Streamlabs Polly")

    def __split_tts(self, path: str, text: str, voice: str):
        parent_path = Path(path).parent
        split_files = []
        split_text = [
            x.group().strip() for x in re.finditer(
                r" *(((.|\n){0," + str(self.max_chars) + "})(\.|.$))", text)
        ]

        offset = 0
        for idy, text_cut in enumerate(split_text):
            #print(f"{idx}-{idy}({offset}): {text_cut}\n")
            if not text_cut or text_cut.isspace():
                offset += 1
                continue
            self.__call_tts(f"{parent_path}-{idy - offset}.part.mp3", text_cut,
                            voice)
            split_files.append(f"{parent_path}-{idy - offset}.part.mp3")

        concatenate_audio_segments(split_files)
        for file in split_files:
            Path(file).unlink()
