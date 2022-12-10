# Automatic Media Downloader

A script that automatically fetches all relevant assets to a Reddit post, TTS, Text and Screenshots. All with pre defined paremetars such as reddit post id, subbreddit, TTS voice etc. To then place all assets in a specified folder for easy access from a video editor. (No this bot does not edit and render the video for you, it is instead an asset management tool, for complete automation of video rendering check out the mentioned tool in section "Motivation")

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

4. Visit the Reddit Apps page. Set up an app that is a "script". Paste any URL in redirect URL. Ex:google.com, then copy all relevant info from your apps list (Your script app should be at the bottom of the page) Note that "client_id" can be seen directly under your bot name (weird looking string of mixed letters and numbers), and your "client_secret" can be found by clicking edit

5. Run main.py and enjoy automated downloading:)

## Future plans

- [ ] Twitter Support
- [x] Reddit Support
- [x] Text Pre-Pocessing 
- [ ] Multithreading (Maybe)
- [x] TTS - Save all content to mp3 files
- [x] Screenshot - Save all content to png files
- [x] Text - Save all content to text files
- [x] Running as a logged in user on: Reddit

