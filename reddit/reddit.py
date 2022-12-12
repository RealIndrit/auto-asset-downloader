from praw.models import MoreComments
from praw.models import Submission
from praw.models.comment_forest import CommentForest

#Maybe uneccessary wrapper classes, but makes the code look much cleaner down the line I hope


class RedditPost:

    def __init__(self, submission: Submission):
        self.id: str = submission.id
        self.locked = submission.locked
        self.url: str = submission.permalink
        self.title: str = submission.title
        self.content: str = submission.selftext
        self.author: str = submission.author
        self.comments: list[RedditPostComment] = self.__parsecomments(
            submission.comments)
        self.pinned: bool = submission.stickied
        self.nsfw: bool = submission.over_18
        self.upvotes: int = submission.score
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
                RedditPostComment(comment.author, comment.stickied,
                                  comment.body, comment.permalink, comment.id))
        return parsed_comments


class RedditPostComment:

    def __init__(self, pinned: bool, author: str, body: str, permalink: str,
                 id: str):
        self.author: str = author
        self.pinned: bool = pinned
        self.content: str = body
        self.permalink: str = permalink
        self.id: str = id

    def length(self) -> int:
        return len(self.content)


# Used in the future for the local reddit post hosting system
class RedditAuthor:

    def __init__(self, name: str, picture_link: str):
        self.name: str = name
        self.picture: str = picture_link
