#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-18

import time
# from util.validator import Check
from util.util_sql import SQLManager
from spider.spider import start_spider
from web.web_server import run as web_run
from config import PARSER_LIST, MAX_CHECK, MAX_DOWNLOAD
from multiprocessing import Queue, Process, Value
import queue

def test(queue1):
    time.sleep(5)
    while True:
        if not queue1.empty():
            print(queue1.qsize())
            print(queue1.get())
        else:
            break

# SQLManager().create()

s = time.time()

q0 = Queue()
q1 = Queue(maxsize=MAX_DOWNLOAD)
q2 = Queue(maxsize=MAX_CHECK)

# p1 = Process(target=web_run)
p2 = Process(target=start_spider, args=(q0,))
# p3 = Process(target=test, args=(q0,))
# p1.start()
p2.start()

# p1.join()
p2.join()
# p3.start()
# p3.join()
# 6.359321355819702
print(time.time()-s)