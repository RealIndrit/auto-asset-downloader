import praw
from prawcore.exceptions import ResponseException
from reddit.reddit import RedditPost
from reddit.reddit_helper import download_reddit_assets
from utils.text_processor import pre_process_text
from utils import settings

def example():
   try:
      reddit = praw.Reddit(
         client_id=settings.config["reddit"]["credentials"]["client_id"],
         client_secret=settings.config["reddit"]["credentials"]["client_secret"],
         user_agent="Accessing Reddit threads",
         username=settings.config["reddit"]["credentials"]["username"],
         passkey=settings.config["reddit"]["credentials"]["password"],
         check_for_async=False,
   )
   except ResponseException as e:
      match e.response.status_code:
         case 401:
            print("Invalid credentials - please check them in config.toml")
   except:
      print("Something went wrong...")


   if settings.config["reddit"]["settings"]["post_id"]:
      print("Post ID found... will override subreddit")
      submission = reddit.submission(
            id=settings.config["reddit"]["settings"]["post_id"])
   else:
      print("Getting subreddit threads...")
      subreddit_choice = settings.config["reddit"]["settings"]["subreddit"]
      print(f"Using subreddit: r/{subreddit_choice} from config")
      if str(subreddit_choice).casefold().startswith("r/"):  # removes the r/ from the input
            subreddit_choice = subreddit_choice[2:]
      subreddit = reddit.subreddit(subreddit_choice)
      submission = subreddit.top(limit=25)[0]

   reddit_post = RedditPost(submission)

   download_reddit_assets(reddit_post, "downloaded", False, True, True, 10, pre_process_text)

if __name__ == "__main__":
    try:
        settings.load_config("config.json")
        example()   
    except Exception as e:
        print("Error!", e)
