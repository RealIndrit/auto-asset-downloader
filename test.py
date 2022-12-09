import json
import praw
from prawcore.exceptions import ResponseException
import re
from reddit.reddit import RedditPost
from reddit.reddit_login import RedditAutomatedLogin
from reddit.reddit_screeeshot import screenshot_comment, screenshot_full_post, screenshot_post_content, screenshot_post_title
from playwright.sync_api import sync_playwright, ViewportSize
from playwright.async_api import async_playwright
from utils import settings

def test():
   try:
      reddit = praw.Reddit(
            client_id=settings.config["client_id"],
            client_secret=settings.config["client_secret"],
            user_agent="Accessing Reddit threads",
            username=settings.config["username"],
            passkey=settings.config["password"],
            check_for_async=False,
      )
   except ResponseException as e:
      match e.response.status_code:
            case 401:
               print("Invalid credentials - please check them in config.toml")
   except:
      print("Something went wrong...")

   # Ask user for subreddit input
   print("Getting subreddit threads...")
   if not settings.config["subreddit"]:  # note to user. you can have multiple subreddits via reddit.subreddit("redditdev+learnpython")
      try:
            subreddit = reddit.subreddit(
               re.sub(
                  r"r\/", "", input("What subreddit would you like to pull from? "))
               # removes the r/ from the input
            )
      except ValueError:
            subreddit = reddit.subreddit("askreddit")
            print("Subreddit not defined. Using AskReddit.")
   else:
      subreddit_choice = settings.config["subreddit"]
      print(f"Using subreddit: r/{subreddit_choice} from config")
      if str(subreddit_choice).casefold().startswith("r/"):  # removes the r/ from the input
            subreddit_choice = subreddit_choice[2:]
      subreddit = reddit.subreddit(subreddit_choice)

   if (
      settings.config["post_id"]
      and len(str(settings.config["post_id"]).split("+")) == 1
   ):
      submission = reddit.submission(
            id=settings.config["post_id"])
   else:
      submission = subreddit.top(limit=25)[0]

   return RedditPost(submission)

settings.load_config("config.json")

reddit_post = test()
with sync_playwright() as p:
   browser = p.chromium.launch(headless=False)
   context = browser.new_context()
   cookies = json.load(
        open("./reddit/data/cookie-dark-mode.json") if settings.config["theme"] ==
        "dark" else open("./reddit/data/cookie-light-mode.json"))

   context.add_cookies(cookies)
   page = context.new_page()
   RedditAutomatedLogin(page, settings.config["username"], settings.config["password"])
   screenshot_post_title(page, reddit_post, f'test/{reddit_post.id}/title.png')
   screenshot_comment(page, reddit_post.comments[0], f'test/{reddit_post.id}/comment.png')
   screenshot_full_post(page, reddit_post, f'test/{reddit_post.id}/full_post.png')
   screenshot_post_content(page, reddit_post, f'test/{reddit_post.id}/content.png')