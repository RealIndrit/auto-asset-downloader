import types
import json
from reddit.reddit import RedditPost
from reddit.reddit_login import RedditAutomatedLogin
from reddit.reddit_screeeshot import screenshot_comment, screenshot_post_full, screenshot_post_content, screenshot_post_title
from playwright.sync_api import sync_playwright, ViewportSize
from tts.streamlabs_tts import StreamlabsPolly
from utils import settings
from pathlib import Path

from utils.utils import append_to_file, write_to_file


def screenshot_post(reddit_post: RedditPost,
                    path: str,
                    comments: int = 0,
                    pre_process_func: types.FunctionType = None):

    print(f'Downloading screenshots')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        cookies = json.load(
            open("./reddit/data/cookie-dark-mode.json"
                 ) if settings.config["reddit"]["settings"]["theme"] ==
            "dark" else open("./reddit/data/cookie-light-mode.json"))

        context.add_cookies(cookies)
        page = context.new_page()
        page.set_viewport_size(ViewportSize(width=1920, height=1080))
        RedditAutomatedLogin(
            page, settings.config["reddit"]["credentials"]["username"],
            settings.config["reddit"]["credentials"]["password"])

        screenshot_post_title(
            page,
            reddit_post,
            Path.joinpath(Path(path),
                          Path(f'{reddit_post.id}/png/post/post_title.png')),
            pre_process_func=pre_process_func)

        screenshot_post_content(
            page,
            reddit_post,
            Path.joinpath(Path(path),
                          Path(f'{reddit_post.id}/png/post/post_content.png')),
            pre_process_func=pre_process_func)

        screenshot_post_full(
            page,
            reddit_post,
            Path.joinpath(Path(path),
                          Path(f'{reddit_post.id}/png/post/post_full.png')),
            pre_process_func=pre_process_func)

        for i, reddit_comment in enumerate(reddit_post.comments):
            if i not in range(comments):
                break

            screenshot_comment(
                page,
                reddit_comment,
                Path.joinpath(
                    Path(path),
                    Path(f'{reddit_post.id}/png/comments/comment_{i}.png')),
                pre_process_func=pre_process_func)


def save_to_text_file(reddit_post: RedditPost,
                      path: str,
                      comments: int,
                      pre_process_func: types.FunctionType = None):

    print(f'Saving to text files')
    title_file = Path(
        Path.joinpath(Path(path),
                      Path(f'{reddit_post.id}/text/post/post_title.txt')))
    title = pre_process_func(
        reddit_post.title) if pre_process_func else reddit_post.title
    write_to_file(title_file, title, "utf-16")

    content_file = Path(
        Path.joinpath(Path(path),
                      Path(f'{reddit_post.id}/text/post/post_content.txt')))
    content = pre_process_func(
        reddit_post.content) if pre_process_func else reddit_post.content
    write_to_file(content_file, content, "utf-16")

    full_file = Path(
        Path.joinpath(Path(path),
                      Path(f'{reddit_post.id}/text/post/post_full.txt')))
    write_to_file(full_file, title + "\n\n", "utf-16")
    append_to_file(full_file, content, "utf-16")

    for i, reddit_comment in enumerate(reddit_post.comments):
        if i not in range(comments):
            break
        comment_file = Path(
            Path.joinpath(
                Path(path),
                Path(f'{reddit_post.id}/text/comment/comment_{i}.txt')))
        content = pre_process_func(
            reddit_comment.content
        ) if pre_process_func else reddit_comment.content
        write_to_file(comment_file, content, "utf-16")


def save_tts(reddit_post: RedditPost,
             path: str,
             comments: int,
             pre_process_func: types.FunctionType = None):

    print(f'Saving to mp3 files')
    title_mp3 = Path(
        Path.joinpath(Path(path),
                      Path(f'{reddit_post.id}/mp3/post/post_title.mp3')))
    title_mp3.parent.mkdir(exist_ok=True, parents=True)
    title = pre_process_func(
        reddit_post.title) if pre_process_func else reddit_post.title
    StreamlabsPolly().run(title, title_mp3)

    content_mp3 = Path(
        Path.joinpath(Path(path),
                      Path(f'{reddit_post.id}/mp3/post/post_content.mp3')))
    content = pre_process_func(
        reddit_post.content) if pre_process_func else reddit_post.content
    if content != "":
        StreamlabsPolly().run(content, content_mp3)

    for i, reddit_comment in enumerate(reddit_post.comments):
        if i not in range(comments):
            break
        comment_file = Path(
            Path.joinpath(
                Path(path),
                Path(f'{reddit_post.id}/mp3/comment/comment_{i}.mp3')))
        comment_file.parent.mkdir(exist_ok=True, parents=True)
        content = pre_process_func(
            reddit_comment.content
        ) if pre_process_func else reddit_comment.content
        StreamlabsPolly().run(content, comment_file)


def download_reddit_assets(reddit_post: RedditPost,
                           path: str,
                           tts: bool,
                           text_file: bool,
                           screenshot: bool,
                           comments: int = 0,
                           pre_process_func: types.FunctionType = None):

    print(f'Downloading: https://reddit.com{reddit_post.url}')
    if screenshot:
        screenshot_post(reddit_post, path, comments, pre_process_func)
    if text_file:
        save_to_text_file(reddit_post, path, comments, pre_process_func)
    if tts:
        save_tts(reddit_post, path, comments, pre_process_func)