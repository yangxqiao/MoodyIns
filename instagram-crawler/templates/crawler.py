# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template
import argparse
import json
import sys
from io import open

from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings
from ToneAnalyzer import toneAnalyzer
from testing import some_func

def usage():
    return '''python crawler.py hashtag -t taiwan -o ./output'''


def get_posts_by_hashtag(tag, number, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data):
    out = json.dumps(data, ensure_ascii=False)
    strings = ""
    urlList = []
    for x in data:
        if 'description' in x and x['description']:
            # print(x['description'])
            strings += x['description']
            strings += " "
        urlList.append(x['img_url'])

    textTone = ""
    if strings:
        textTone = toneAnalyzer(strings)
    imgTone = some_func(urlList) #a list of emotions: {happiness: 0.2 ....bluh}
    print("printing imgtone")
    print(imgTone)
    print("printing textTone")
    if textTone:
        print(textTone)
    return [imgTone, textTone]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
    parser.add_argument(
        "mode", help="options: [hashtag]"
    )
    parser.add_argument("-n", "--number", type=int, help="number of returned posts")
    parser.add_argument("-t", "--tag", help="instagram's tag name")
    parser.add_argument("-o", "--output", help="output file name(json format)")
    parser.add_argument("--debug", action="store_true")

    prepare_override_settings(parser)

    args = parser.parse_args()

    override_settings(args)

    if args.mode == "hashtag":
        arg_required("tag")
        output(
            get_posts_by_hashtag(args.tag, args.number or 100, args.debug)
        )
    else:
        usage()
