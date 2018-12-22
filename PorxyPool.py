#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-18


from util.validator import start_check
from util.util_sql import SQLManager
from spider.spider import start_spider
from web.web_server import web_run
from config import MAX_CHECK, MAX_DOWNLOAD
from multiprocessing import Queue, Process


SQLManager().create()

q0 = Queue()
q1 = Queue(maxsize=MAX_DOWNLOAD)
q2 = Queue(maxsize=MAX_CHECK)

p1 = Process(target=web_run)
p2 = Process(target=start_spider, args=(q0,))
p3 = Process(target=start_check, args=(q0,))

p1.start()
p2.start()
p3.start()

p1.join()
p2.join()
p3.join()
