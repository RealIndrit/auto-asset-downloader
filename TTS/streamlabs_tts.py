from json import JSONDecodeError
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import urllib.parse
import urllib.response
import random
import re

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

    def run(self, path: str, text: str, voice: str):
        if voice.upper == "RANDOM":
            voice = self.randomvoice()
        text = sanitize_text(text)

        if len(text) > self.max_chars:
            #self.__split_tts(path, text, voice)
            pass
        else:
            self.__call_tts(path, text, voice)

    def randomvoice(self):
        return random.choice(self.voices)

    def __call_tts(self, path: str, text: str, voice: str):
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'
        }
        data = {"voice": voice, "text": text, "service": "polly"}

        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self.url, data=data, headers=headers)
        try:
            response = urllib.request.urlopen(req)
            try:
                req = urllib.request.Request(url=json.loads(
                    response.read())["speak_url"],
                                             headers=headers)
                voice_data = urllib.request.urlopen(req)
                with open(path, "wb") as f:
                    f.write(voice_data.read())
            except (KeyError, JSONDecodeError):
                try:
                    if json.loads(
                            response.read())["error"] == "No text specified!":
                        raise ValueError(
                            "Please specify a text to convert to speech.")
                except (KeyError, JSONDecodeError):
                    print("Error occurred calling Streamlabs Polly")
        except urllib.error.HTTPError as error:
            if not check_ratelimit(error):
                self.__call_tts(path, text, voice)
            else:
                print("HTTPError", error)

    def __split_tts(self, path: str, text: str, voice: str):
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
            temp_path = os.path.dirname(path)
            temp_path = os.path.join(
                temp_path, f"comment_segment_{idy - offset}.part.mp3")
            self.__call_tts(temp_path, text_cut, voice)
            split_files.append(temp_path)

        concatenate_audio_segments(split_files, path)
        for file in split_files:
            Path(file).unlink()
