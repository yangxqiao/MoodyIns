from __future__ import unicode_literals

import glob
import json
import os
import re
import sys
import time
import traceback
from builtins import open
from time import sleep

from tqdm import tqdm

from . import secret
from .browser import Browser
from .exceptions import RetryException
from .fetch import fetch_details
from .utils import instagram_int
from .utils import randmized_sleep
from .utils import retry

import urllib.request, json 


class Logging(object):
    PREFIX = "instagram-crawler"

    def __init__(self):
        try:
            timestamp = int(time.time())
            self.cleanup(timestamp)
            self.logger = open("/tmp/%s-%s.log" % (Logging.PREFIX, timestamp), "w")
            self.log_disable = False
        except Exception:
            self.log_disable = True

    def cleanup(self, timestamp):
        days = 86400 * 7
        days_ago_log = "/tmp/%s-%s.log" % (Logging.PREFIX, timestamp - days)
        for log in glob.glob("/tmp/instagram-crawler-*.log"):
            if log < days_ago_log:
                os.remove(log)

    def log(self, msg):
        if self.log_disable:
            return

        self.logger.write(msg + "\n")
        self.logger.flush()

    def __del__(self):
        if self.log_disable:
            return
        self.logger.close()

class InsCrawler(Logging):
    URL = "https://www.instagram.com"
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0

    def get_latest_posts_by_tag(self, tag, num):
        url = "%s/explore/tags/%s/" % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_posts(num)

    def _get_posts(self, num):
        """
            To get posts, we have to click on the load more
            button and make the browser call post api.
        """
        TIMEOUT = 600
        browser = self.browser
        key_set = set()
        post_url = []
        posts = []
        pre_post_num = 0
        wait_time = 1

        pbar = tqdm(total=num)

        '''Update 03/13/2020'''
        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find(".v1Nh3 a")

            for ele in ele_posts:
                key = ele.get_attribute("href")
                post_url.append(key)
                
                print(key)
                if key not in key_set:
                    dict_post = {"key": key}
                    ele_img = browser.find_one(".KL4Bh img", ele)
                    dict_post["img_url"] = ele_img.get_attribute("src")
                    
                    url = urllib.request.urlopen(key + "?__a=1")
                    data = json.loads(url.read().decode())
                    print(data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"])
                    # # Update 03/13/2020: make another browser and crawl
                    # caption = ""
                    # try:
                    #     second_browser = Browser(has_screen=False)
                    #     second_browser.get(key)
                    #     caption = second_browser.find_one(".C4VMK").find_element_by_tag_name("span").text
                    #     print("caption: ", caption)
                    # except Exception:
                    #     try:
                    #         caption = second_browser.find_one(".C4VMK").find_element_by_tag_name("h1").text
                    #         print("caption: ", caption)
                    #     except Exception:
                    #         caption = ele_img.get_attribute("alt")
                    dict_post["caption"] = data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                    # # Update 03/13/2020: Update finish
                    fetch_details(browser, dict_post)

                    key_set.add(key)
                    posts.append(dict_post)

                    if len(posts) == num:
                        break

            if pre_post_num == len(posts):
                pbar.set_description("Wait for %s sec" % (wait_time))
                sleep(wait_time)
                pbar.set_description("fetching")

                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(posts)
            browser.scroll_down()

            return pre_post_num, wait_time, post_url
        pbar.set_description("fetching")
        while len(posts) < num and wait_time < TIMEOUT:
            post_num, wait_time, post_url = start_fetching(pre_post_num, wait_time)
            pbar.update(post_num - pre_post_num)
            pre_post_num = post_num

            loading = browser.find_one(".W1Bne")
            if not loading and wait_time > TIMEOUT / 2:
                break

        pbar.close()
        print("Done. Fetched %s posts." % (min(len(posts), num)))
        return [posts[:num], post_url]

#get_latest_posts_by_tag("beauty", 5)