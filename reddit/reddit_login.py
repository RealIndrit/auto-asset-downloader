import json

from playwright._impl._page import Page

LOGIN_URL = "https://reddit.com/login"


class RedditAutomatedLogin:

    def __init__(self,
                 page: Page,
                 username: str,
                 password: str,
                 custom_cookies: json = []) -> bool:
        self.custom_cookies = custom_cookies
        self.__get_session_cookies(page, username, password)

    def __get_session_cookies(self, page: Page, username: str, password: str):
        try:
            page.context.add_cookies(self.custom_cookies)
            page.goto(LOGIN_URL, timeout=0)
            page.type("[name=username]", username)
            page.type("[name=password]", password)
            page.get_by_role("button", name="Log In").click()
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print("Something went wrong:", e)
