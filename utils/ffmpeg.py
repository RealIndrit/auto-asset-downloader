from pathlib import Path
import os
import zipfile
from utils import settings
import subprocess
import urllib.request

FFMPEG_BINARIES = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
FFMPEG_FOLDER_DEFAULT = "./ffmpeg/"


class FFMPEG:

    def __init__(self, verbose=False):
        self.__resolve_ffmpeg()
        self.verbose = verbose

    def run_ffmpeg(self, *args):
        cmd = [settings.config["global"]["ffmpeg"]["ffplay"]]
        if not self.verbose:
            cmd = cmd + ["-loglevel", "repeat+level+error"]
        cmd = cmd + list(args)
        subprocess.run(cmd)

    def run_ffprobe(self, *args):
        cmd = [settings.config["global"]["ffmpeg"]["ffprobe"]] + list(args)
        if not self.verbose:
            cmd = cmd + ["-loglevel", "repeat+level+error"]
        cmd = cmd + list(args)
        subprocess.run(cmd)

    def run_ffplay(self, *args):
        cmd = [settings.config["global"]["ffmpeg"]["ffplay"]] + list(args)
        if not self.verbose:
            cmd = cmd + ["-loglevel", "repeat+level+error"]
        cmd = cmd + list(args)
        print(cmd)
        subprocess.run(cmd)

    def __install_ffmpeg(self, url: str, output: str):
        temp_file = "ffmpeg.zip"
        print(f"Downloading {temp_file}")
        urllib.request.urlretrieve(url, temp_file)
        print(f"Downloaded {temp_file}")

        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            print(f"Extracting {temp_file}")
            zip_ref.extractall(output)
        Path(temp_file).unlink()
        print(f"Extracted {temp_file} to {output}")
        return Path(
            os.path.join(FFMPEG_FOLDER_DEFAULT,
                         "fmpeg-master-latest-win64-gpl-shared", "bin"))

    def __resolve_ffmpeg(self):
        #ffmpeg binaries paths not defined, assuming no installation -> Install it
        if (not settings.config["global"]["ffmpeg"]["ffmpeg"]
                or not settings.config["global"]["ffmpeg"]["ffprobe"]
                or not settings.config["global"]["ffmpeg"]["ffplay"]):
            ffmpeg_path = self.__install_ffmpeg(FFMPEG_BINARIES,
                                                FFMPEG_FOLDER_DEFAULT)
            settings.config["global"]["ffmpeg"]["ffmpeg"] = os.path.join(
                ffmpeg_path, "ffmpeg.exe")
            settings.config["global"]["ffmpeg"]["ffprobe"] = os.path.join(
                ffmpeg_path, "ffprobe.exe")
            settings.config["global"]["ffmpeg"]["ffplay"] = os.path.join(
                ffmpeg_path, "ffplay.exe")