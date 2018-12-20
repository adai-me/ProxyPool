#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-13


from gevent import monkey
monkey.patch_all()

import random
import chardet
import requests
import gevent

from config import USER_AGENTS, TIMEOUT, NUM_RETRIES, CHINA_AREA, PARSER_LIST
from util.util_sql import SQLManager
from util.validator import Check


def get_header():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate"
    }

def download(url):
    try:
        print("Downloading %s" % url)
        r = requests.get(url=url, headers=get_header(), timeout=TIMEOUT)
        r.encoding = chardet.detect(r.content)["encoding"]
        if (not r.ok) or len(r.content) < 500:
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

                r = requests.get(url=url, headers=get_header(), timeout=TIMEOUT, proxies=proxies)
                r.encoding = chardet.detect(r.content)["encoding"]
                if (not r.ok) or len(r.content) < 500:
                    raise ConnectionError
                else:
                    return r.text
            except Exception:
                count += 1

    return None


def crawl(parser):
    # proxy_list = []
    for url in parser["urls"]:
        response = download(url)
        if response:
            prowies = Parser().parse(response, parser)
            for proxy in prowies:
                # proxy_list.append(proxy)
                if Check().live(proxy):
                    proxy["score"] = 10
                    SQLManager().insert(proxy)

    # return proxy_list


def test():
    # url = "https://www.kuaidaili.com/proxylist/1"
    # response = download(url)
    # parser = PARSER_LIST[0]
    # prowies = Parser().parse(response, parser)
    # print(prowies[0])
    # url = "http://ip.taobao.com/service/getIpInfo.php?ip=210.75.225.254"
    # print(requests.get(url))
    SQLManager().drop()
    SQLManager().create()
    crawl(PARSER_LIST[0])


if __name__ == "__main__":
    test()