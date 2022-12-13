import types
from playwright._impl._page import Page
from reddit.reddit import RedditPost, RedditPostComment

# All html element id's that the screenshot tool is targeting can be seen here, as long as these id's exsists
# in template/post.html or template/commnet.html, the tool will work properly!

TIMESTAMP_QUERY = 'document.querySelector(`#time`).innerText'
TITLE_QUERY = 'document.querySelector(`#title`).innerText'
TEXT_QUERY = 'document.querySelector(`#text`).innerHTML'
AUTHOR_NAME_QUERY = 'document.querySelector(`#author_name`).innerText'
AUTHOR_PICTURE_QUERY = 'document.querySelector(`#author_picture`).innerText'
VOTE_QUERY = 'document.querySelector(`#votes`).innerText'
NSWF_QUERY = 'document.querySelector(`#nsfw`).innerText'


def screenshot_post_full(page: Page,
                         post: RedditPost,
                         path: str,
                         pre_process_func: types.FunctionType = None) -> bool:

    try:
        page.goto(f'localhost:5500/reddit/templates/post.html', timeout=0)
        title: str = post.title
        text: str = post.content
        votes: str = post.upvotes
        author: str = post.author

        if pre_process_func:
            title = pre_process_func(title)
            text = pre_process_func(text)
        text = __build_text_container(text)
        page.evaluate(
            f'title => {TITLE_QUERY} = title',
            title,
        )
        page.evaluate(
            f'votes => {VOTE_QUERY} = votes',
            votes,
        )
        page.evaluate(
            f'author => {AUTHOR_NAME_QUERY} = author',
            f"u/{author}",
        )
        page.evaluate(
            f"text => {TEXT_QUERY} = text",
            text,
        )
        page.locator(f"#body").screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True


def screenshot_post_title(page: Page,
                          post: RedditPost,
                          path: str,
                          pre_process_func: types.FunctionType = None) -> bool:

    try:
        page.goto(f'localhost:5500/reddit/templates/post.html', timeout=0)
        title: str = post.title
        if pre_process_func:
            title = pre_process_func(title)
        page.evaluate(
            f'title => {TITLE_QUERY} = title',
            title,
        )
        page.locator(f"#title").screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True


def screenshot_post_content(
        page: Page,
        post: RedditPost,
        path: str,
        pre_process_func: types.FunctionType = None) -> bool:

    try:
        page.goto(f'localhost:5500/reddit/templates/post.html', timeout=0)
        text: str = post.content
        if pre_process_func:
            text = pre_process_func(text)
        text = __build_text_container(text)
        page.evaluate(
            f"text => {TEXT_QUERY} = text",
            text,
        )
        page.locator(f"#text").screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True


def screenshot_comment(page: Page,
                       comment: RedditPostComment,
                       path: str,
                       pre_process_func: types.FunctionType = None) -> bool:

    try:
        page.goto(f'localhost:5500/reddit/templates/comment.html', timeout=0)
        text: str = comment.content
        votes: str = comment.upvotes
        author: str = comment.author

        if pre_process_func:
            text = pre_process_func(text)
        text = __build_text_container(text)
        page.evaluate(
            f'votes => {VOTE_QUERY} = votes',
            votes,
        )
        page.evaluate(
            f'author => {AUTHOR_NAME_QUERY} = author',
            f"u/{author}",
        )
        page.evaluate(
            f"text => {TEXT_QUERY} = text",
            text,
        )
        page.locator(f"#body").screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True


def __build_text_container(text: str) -> str:
    paragraphs = text.split("\n")
    html = []
    for p in paragraphs:
        html.append(f"\n<p>{p}</p>")
    return ' '.join(html)
