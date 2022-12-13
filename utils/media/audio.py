import os
from pathlib import Path
from utils.ffmpeg import FFMPEG
from utils.utils import append_to_file


def concatenate_audio_segments(audio_segments: list[str], concat_audio: str):
    """
      Pass on the arguments to the ffmpeg wrapper in list type
      
      Args:
        audio_segments_file (str): path to concat list text file
        output (str): path to where to dump the concatenated audiofile

      Returns:
        NoneType
    """
    parent_path = os.path.dirname(concat_audio)
    audio_segments_file = os.path.join(parent_path, "concat.mp3.txt")
    for file in audio_segments:
        append_to_file(audio_segments_file, f"file '{file}'\n")

    FFMPEG().run_ffmpeg([
        "-f", "concat", "-i", audio_segments_file, "-c:a", "copy", "-y",
        concat_audio
    ])

    Path(audio_segments_file).unlink()
    for file in audio_segments:
        Path(os.path.join(parent_path, file)).unlink()
