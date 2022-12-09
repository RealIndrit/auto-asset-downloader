import json
from playwright.playwright_helper import create_playwright_session, close_playwright_session

from reddit.reddit_login import RedditAutomatedLogin
from utils import settings


def main():
    cookies = json.load(
        open("cookie-dark-mode.json") if config["theme"] ==
        "dark" else open("cookie-light-mode.json"))

    pbc = create_playwright_session()
    pbc.add_cookies(cookies)
    page = pbc.new_page()
    RedditAutomatedLogin(page, config["username"], config["password"])
    page.goto("https://reddit.com/zfsfzj", timeout=0)


if __name__ == "__main__":
    try:
        config = settings.load_config("config.json")
        main()
    except Exception as e:
        print("Error!", e)
        close_playwright_session()
