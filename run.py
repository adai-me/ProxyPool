#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-18

# from util.validator import Check
from util.util_sql import SQLManager
from spider.crawl import crawl
from web.web_server import run as web_run
from config import PARSER_LIST
from multiprocessing import Queue, Process, Value


SQLManager().create()

def spider_run():
    for parser in PARSER_LIST:
        print(parser)
        crawl(parser)


p1 = Process(target=web_run)
p2 = Process(target=spider_run)
p1.start()
p2.start()