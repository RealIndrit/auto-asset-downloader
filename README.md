# Automatic Video Asset Downloader

A script that automatically fetches all relevant assets to a Reddit post, TTS, Text and Screenshots. All with pre defined paremetars such as reddit post id, subbreddit, TTS voice etc. To then place all assets in a specified folder for easy access from a video editor. (No this bot does not edit and render the video for you, it is instead an asset managment tool, for complete automation of video rendering check out the mentioned tool in section "Motivation")

## Motivation

Inspired by the [Reddit Video Maker Bot](https://github.com/elebumm/RedditVideoMakerBot) project, initially I had the plan to PR the changes, but after realising 
the PR would comepletely re-write the system from the ground up and probbaly confuse a lot of the maintainers, I decided to just make it a separete project instead.

## Disclaimers

- **At the moment**, this repository will not be able to fetch assets from other platforms than Reddit, I am planning to add Twitter in the future, and if I have time
or energy maybe even add multithreading support for that extra speed.

## Requirements

- Python 3.11+
- Playwright (this should install automatically in installation)

## Installation

1. Clone this repository
2. Run `pip install -r requirements.txt`

3. Run `python -m playwright install` and `python -m playwright install-deps`


## Future plans

- [ ] Twitter Support
- [ ] Automatic Text censoring 
- [ ] Multithreading (Maybe)
- [x] TTS
- [x] Screenshot
- [ ] Save text to text files
- [x] Running as a logged in user on Reddit

