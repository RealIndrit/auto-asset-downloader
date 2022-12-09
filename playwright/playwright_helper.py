from playwright.sync_api import sync_playwright, ViewportSize
from playwright.async_api import async_playwright
from playwright.sync_api._generated import BrowserContext

pbc = None
pb = None


def create_playwright_session() -> BrowserContext:
    global pbc
    global pb
    p = sync_playwright()
    pb = p.chromium.launch()
    pbc = pb.new_context()
    return pbc


def close_playwright_session():
    pbc.close()
    pb.close()
