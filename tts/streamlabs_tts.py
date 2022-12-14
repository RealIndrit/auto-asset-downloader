from json import JSONDecodeError
import json
import os
import urllib.error
import urllib.request
import urllib.parse
import urllib.response
import random
import re

from tts.tts_helper import check_ratelimit, sanitize_text
from utils.media.audio import concatenate_audio_segments

# Credits: https://github.com/elebumm/RedditVideoMakerBot/blob/master/TTS/streamlabs_polly.py

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
        """
         Passes the text through a filter, and then send it off to either streamlabs tts service directly
         or send its off to the split tts for longer text tts

         Args:
             path (str): Text to be sanitized
             text (str): Text to be sanitized and then sent through tts
             voice: (str): What voice the tts should use see "voices" in the top of file for available voices, or picks 
               random voice if voice is set to RANDOM

         Returns:
            NoneType
        """
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
        """
         Send post request to streamlabs tts service, with fake header and payload of, voice, text and service type. Fetches the time limited 
         tts url and downloads the tts file. If rate limited, run rate limit function and call self again to complete the tts

         Args:
             path (str): Text to be sanitized
             text (str): Text to be sanitized and then sent through tts
             voice: (str): What voice the tts should use see "voices" in the top of file for available voices

         Returns:
            NoneType
        """
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
        """
         Splits text for the tts into sections of full scentences within the max cahracter limit, and send each sub section of the text into its own tts tracked file, 
         writes the tracked files into a text file for ffmpeg to read for the concatenation, see https://trac.ffmpeg.org/wiki/Concatenate, lastly clean
         up all temp files (audio files and text file)

         Args:
             path (str): Path of output audio file
             text (str): Text to be sanitized and then sent through tts
             voice: (str): What voice the tts should use see "voices" in the top of file for available voices, or picks 
               random voice if voice is set to RANDOM

         Returns:
            NoneType
        """
        audio_segments = []
        text_segments = [
            x.group().strip() for x in re.finditer(
                r" *(((.|\n){0," + str(self.max_chars) + "})(\.|.$))", text)
        ]

        offset = 0
        parent_path = os.path.dirname(path)
        for idy, text_cut in enumerate(text_segments):
            #print(f"{idx}-{idy}({offset}): {text_cut}\n")
            if not text_cut or text_cut.isspace():
                offset += 1
                continue

            temp_name = f"audio_segment_{idy - offset}.part.mp3"
            temp_path = os.path.join(parent_path, temp_name)
            self.__call_tts(temp_path, text_cut, voice)
            audio_segments.append(temp_name)

        concatenate_audio_segments(audio_segments, path)
