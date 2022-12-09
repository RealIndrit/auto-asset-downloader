from playwright._impl._page import Page

from reddit.reddit import RedditPost, RedditPostComment
from utils.text_processor import pre_process_text


def screenshot_comment(page: Page,
                       comment: RedditPostComment,
                       path: str,
                       pre_process=False) -> bool:
    try:
        page.goto(f'https://reddit.com{comment.permalink}', timeout=0)
        if pre_process:
            content = pre_process_text(comment.content)
            page.evaluate(
                '([tl_content, tl_id]) => document.querySelector(`#t1_${tl_id} > div:nth-child(2) > div > div[data-testid="comment"] > div`).textContent = tl_content',
                [content, comment.id],
            )
        page.locator(f"#t1_{comment.id}").screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    print("Screenshots downloaded Successfully.")
    return True


def screenshot_post_title(page: Page,
                          post: RedditPost,
                          path: str,
                          pre_process=False) -> bool:
    try:
        page.goto(f'https://reddit.com{post.url}', timeout=0)
        if pre_process:
            title = pre_process_text(post.title)
            page.evaluate(
                "tl_content => document.querySelector('[data-adclicklocation=\"title\"] > div:nth-child(3) > div > div').textContent = tl_content",
                title,
            )
        page.locator('[data-adclicklocation="title"]').screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True


def screenshot_post_content(page: Page,
                            post: RedditPost,
                            path: str,
                            pre_process=False) -> bool:
    try:
        page.goto(f'https://reddit.com{post.url}', timeout=0)
        if page.get_by_role("button", name="Click to see nsfw").is_visible():
            page.get_by_role("button", name="Click to see nsfw").click()
        if pre_process:
            content = pre_process_text(post.content)
            print("Revealing post content")
            page.evaluate(
                "tl_content => document.querySelector('[data-click-id=\"text\"] > div:nth-child(3) > div > div').textContent = tl_content",
                content,
            )
        page.locator('[data-click-id="text"]').screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True


def screenshot_full_post(page: Page,
                         post: RedditPost,
                         path: str,
                         pre_process=False) -> bool:
    try:
        page.goto(f'https://reddit.com{post.url}', timeout=0)
        if page.get_by_role("button", name="Click to see nsfw").is_visible():
            page.get_by_role("button", name="Click to see nsfw").click()
            print("Revealing post content")
        if pre_process:
            title = pre_process_text(post.title)
            content = pre_process_text(post.content)
            page.evaluate(
                "tl_content => document.querySelector('[data-adclicklocation=\"title\"] > div:nth-child(3) > div > div').textContent = tl_content",
                title,
            )
            page.evaluate(
                "tl_content => document.querySelector('[data-click-id=\"text\"] > div:nth-child(3) > div > div').textContent = tl_content",
                content,
            )
        page.locator('[data-testid = "post-container"]').screenshot(path=path)
    except TimeoutError:
        print("TimeoutError: Skipping screenshot...")
        return False
    return True
