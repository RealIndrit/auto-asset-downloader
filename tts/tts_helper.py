import re
import sys
from datetime import datetime, timezone
import time as pytime
from time import sleep
from urllib.error import HTTPError
from utils.ffmpeg import FFMPEG


def concatenate_audio_segments(audio_segments_file: str, output: str):
    """
      Pass on the arguments to the ffmpeg wrapper in list type
      
      Args:
        audio_segments_file (str): path to concat list text file
        output (str): path to where to dump the concatenated audiofile

      Returns:
        NoneType
    """
    FFMPEG().run_ffmpeg([
        "-f", "concat", "-i", audio_segments_file, "-c:a", "copy", "-y", output
    ])


# Credits https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/voice.py
def check_ratelimit(response: HTTPError):
    """
      Checks if the response is a ratelimit response.
      If it is, it sleeps for the time specified in the response.

      Args:
        response (HTTPError): response content of request

      Returns:
        NoneType
    """
    if response.code == 429:
        try:
            time = int(response.headers["X-RateLimit-Reset"])
            print(
                f"Ratelimit hit. Sleeping for {time - int(pytime.time())} seconds."
            )
            sleep_until(time)
            return False
        except KeyError:  # if the header is not present, we don't know how long to wait
            return False

    return True


# Credits https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/voice.py
def sleep_until(time: int | datetime):
    """
      Pause your program until a specific end time.

      Args:
        time (int or datetime): is either a valid datetime object or unix timestamp in seconds (i.e. seconds since Unix epoch)
      
      Returns:
        NoneType
    """
    end = time

    # Convert datetime to unix timestamp and adjust for locality
    if isinstance(time, datetime):
        # If we're on Python 3 and the user specified a timezone, convert to UTC and get the timestamp.
        if sys.version_info[0] >= 3 and time.tzinfo:
            end = time.astimezone(timezone.utc).timestamp()
        else:
            zoneDiff = pytime.time() - (datetime.now() -
                                        datetime(1970, 1, 1)).total_seconds()
            end = (time - datetime(1970, 1, 1)).total_seconds() + zoneDiff

    # Type check
    if not isinstance(end, (int, float)):
        raise Exception(
            "The time parameter is not a number or datetime object")

    # Now we wait
    while True:
        now = pytime.time()
        diff = end - now

        #
        # Time is up!
        #
        if diff <= 0:
            break
        else:
            # 'logarithmic' sleeping to minimize loop iterations
            sleep(diff / 2)


# Credits https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/voice.py
def sanitize_text(text: str) -> str:
    """
      Sanitizes the text for tts.
        What gets removed:
      - following characters`^_~@!&;#:-%“”‘"%*/{}[]()\|<>?=+`
      - any http or https links

      Args:
         text (str): Text to be sanitized

      Returns:
         str: Sanitized text
    """

    # remove any urls from the text
    regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

    result = re.sub(regex_urls, " ", text)

    # note: not removing apostrophes
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@;#\-–—%“”‘\"%\*/{}\[\]\(\)\\|<>]"
    result = re.sub(regex_expr, " ", result)
    result = result.replace("+", "plus").replace("&", "and")
    # remove extra whitespace
    return " ".join(result.split())
