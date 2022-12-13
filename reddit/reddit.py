from praw.models import MoreComments, Submission, Redditor
from praw.models.comment_forest import CommentForest

from utils.utils import beautify_number
#Maybe uneccessary wrapper classes, but makes the code look much cleaner down the line I hope


class RedditPost:

    def __init__(self, submission: Submission):
        self.id: str = submission.id
        self.locked = submission.locked
        self.url: str = submission.permalink
        self.title: str = submission.title
        self.content: str = submission.selftext
        self.author: str = self.__check_valid_author(submission.author)
        self.comments: list[RedditPostComment] = self.__parsecomments(
            submission.comments)
        self.pinned: bool = submission.stickied
        self.nsfw: bool = submission.over_18
        self.upvotes: int = beautify_number(submission.score)
        self.ratio = submission.upvote_ratio * 100

    def get_comments_total(self) -> int:
        return len(self.comments)

    def get_comment(self, index: int):
        return self.comments[index]

    def __parsecomments(self, comments: CommentForest) -> list:
        parsed_comments = []
        for comment in comments:
            if isinstance(comment, MoreComments):
                continue  # Dont want nested comments for now (add support for this later I guess)

            if comment.body in ["[removed]", "[deleted]"]:
                continue  # Ignore deleted comments
            parsed_comments.append(
                RedditPostComment(comment.stickied,
                                  self.__check_valid_author(comment.author),
                                  beautify_number(comment.score), comment.body,
                                  comment.permalink, comment.id))
        return parsed_comments

    def __check_valid_author(self, author: Redditor) -> str:
        if not author:
            return "[deleted]"
        return author.name


class RedditPostComment:

    def __init__(self, pinned: bool, author: str, upvotes: str, body: str,
                 permalink: str, id: str):
        self.author: str = author
        self.pinned: bool = pinned
        self.upvotes: str = upvotes
        self.content: str = body
        self.permalink: str = permalink
        self.id: str = id

    def length(self) -> int:
        return len(self.content)