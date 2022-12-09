from praw.models import MoreComments
from praw.models import Submission

#Maybe uneccessary wrapper classes, but makes the code look much cleaner donw the line I hope


class RedditPost:

    def __init__(self, submission: Submission) -> None:
        self.submissionid: str = submission.id
        self.locked = submission.locked
        self.url: str = submission.permalink
        self.title: str = submission.title
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

    def __parsecomments(self, comments):
        parsed_comments = []
        for top_level_comment in comments:
            if isinstance(top_level_comment, MoreComments):
                continue  # Dont want nested comments for now (add support for this later I guess)

            if top_level_comment.body in ["[removed]", "[deleted]"]:
                continue  # Ignore deleted comments

            parsed_comments.append(
                RedditPostComment(top_level_comment.author,
                                  top_level_comment.stickied,
                                  top_level_comment.body,
                                  top_level_comment.permalink,
                                  top_level_comment.id))
        return parsed_comments


class RedditPostComment:

    def __init__(self, pinned, author, body, permalink, id):
        self.author: str = author
        self.pinned: bool = pinned
        self.content: str = body
        self.permalink: str = permalink
        self.id: str = id

    def length(self):
        return len(self.content)
