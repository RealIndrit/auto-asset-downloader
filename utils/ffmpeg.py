from pathlib import Path
import os
import zipfile
from utils import settings
import subprocess
import urllib.request

# Official build mirror, read: https://ffmpeg.org/download.html
FFMPEG_BINARIES = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_FOLDER_DEFAULT = "./ffmpeg/"


class FFMPEG:

    def __init__(self, verbose=False):
        self.__resolve_ffmpeg()
        self.ffmpeg = settings.config["global"]["ffmpeg"]["ffmpeg"]
        self.ffprobe = settings.config["global"]["ffmpeg"]["ffprobe"]
        self.ffplay = settings.config["global"]["ffmpeg"]["ffplay"]
        self.verbose = verbose

    def run_ffmpeg(self, *args):
        cmd = self.__argument_helper(self.ffmpeg, args)
        subprocess.run(cmd)

    def run_ffprobe(self, *args):
        cmd = self.__argument_helper(self.ffprobe, args)
        subprocess.run(cmd)

    def run_ffplay(self, *args):
        cmd = self.__argument_helper(self.ffplay, args)
        subprocess.run(cmd)

    def __argument_helper(self, executable, args) -> list[str]:
        """
         Convert arguments to list tipe and appends it after executable and log flags

         Returns:
            NoneType
        """
        # Lets us pass a list as args
        if len(args) == 1:
            args = list(args[0])
        cmd = [executable]
        if not self.verbose:
            cmd = cmd + ["-loglevel", "repeat+level+error"]
        return cmd + list(args)

    def __install_ffmpeg(self, url: str, output: str) -> Path:
        """
         Downloads, unzips, and installs ffmpeg, also adds ffmpeg executables paths to the config

         Args:
            url (str): url to the build of ffmpeg
            output (str): path to where to install ffmpeg build

         Returns:
            Path type of the path to the output folder where the executables are located
        """

        temp_file = "ffmpeg.zip"
        print(f"Downloading {temp_file}")
        urllib.request.urlretrieve(url, temp_file)
        print(f"Downloaded {temp_file}")

        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            print(f"Extracting {temp_file}")
            zip_ref.extractall(output)
        Path(temp_file).unlink()
        print(f"Extracted {temp_file} to {output}")

        # Will always be the same, as we always download the latest master branch build...
        return Path(
            os.path.join(FFMPEG_FOLDER_DEFAULT,
                         "ffmpeg-master-latest-win64-gpl", "bin"))

    def __resolve_ffmpeg(self):
        """
         Checks config for ffpmeg paths, if not all found, force install and then set the 
         config paths to the installed executables

         Returns:
            NoneType
        """
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