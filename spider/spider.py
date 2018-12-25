#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-13


from gevent import monkey; monkey.patch_all()

import random
import chardet
import requests
import gevent

from config import USER_AGENTS, TIMEOUT, NUM_RETRIES, PARSER_LIST, MAX_DOWNLOAD
from util.util_sql import SQLManager
from util.html_parser import Parser


class Spider():
    def __init__(self, queue):
        self.queue = queue

    def get_header(self):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate"
        }

    def download(self, url):
        try:
            print("Downloading %s" % url)
            r = requests.get(url=url, headers=self.get_header(), timeout=TIMEOUT)
            r.encoding = chardet.detect(r.content)["encoding"]
            if (not r.ok) or len(r.content) < 300:
                raise ConnectionError
            else:
                return r.text

        except Exception:
            count = 0  # 重试次数
            proxy_list = SQLManager().select(10)
            if not proxy_list:
                return None

            while count < NUM_RETRIES:
                try:
                    proxy = random.choice(proxy_list)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=self.get_header(), timeout=TIMEOUT, proxies=proxies)
                    r.encoding = chardet.detect(r.content)["encoding"]
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None

    def crawl(self, parser):
        for url in parser["urls"]:
            response = self.download(url)
            if response:
                proxies = Parser().parser(response, parser)
                for proxy in proxies:
                    # print(proxy)
                    self.queue.put(proxy)
                    # while True:
                    #     if self.queue.full():
                    #         time.sleep(0.5)
                    #     else:
                    #         self.queue.put(proxy)
                    #         break

    def run(self):
        spawns = []
        for parser in PARSER_LIST:
            # self.crawl(parser)
            spawns.append(gevent.spawn(self.crawl, parser))
            if len(spawns) >= MAX_DOWNLOAD:
                gevent.joinall(spawns)
                spawns = []
        gevent.joinall(spawns)


def start_spider(queue):
    spider = Spider(queue)
    spider.run()


def test():
    for parser in PARSER_LIST[2:3]:
        Spider().crawl(parser)


if __name__ == "__main__":
    test()