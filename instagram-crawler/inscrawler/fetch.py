import re
from time import sleep

from .settings import settings

def fetch_initial_comment(browser, dict_post):
    comments_elem = browser.find_one("ul.XQXOT")
    first_post_elem = browser.find_one(".ZyFrc", comments_elem)
    caption = browser.find_one("span", first_post_elem)
    # caption = browser.find_one("span")

    if caption:
        dict_post["description"] = caption.text


def fetch_details(browser, dict_post):
    if not settings.fetch_details:
        return

    browser.open_new_tab(dict_post["key"])

    fetch_initial_comment(browser, dict_post)

    browser.close_current_tab()
