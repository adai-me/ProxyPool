#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-13

import random
import re

from lxml import etree
import chardet
import requests

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


def if_cn(addr):
    # 用来判断地址是否为中国
    for area in CHINA_AREA:
        if area in addr:
            return True
    return False


class Parser():
    def __init__(self):
        pass

    def parse(self, response, parser):
        if parser["type"] == "xpath":
            return self.xpath_praser(response, parser)
        elif parser["type"] == "regular":
            return self.regular_parser(response, parser)
        elif parser["type"] == "module":
            return getattr(self, parser["moduleName"], None)(response, parser)
        else:
            return None

    def xpath_praser(self, response, parser):
        """
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        """
        proxy_list = []
        root = etree.HTML(response)
        proxies = root.xpath(parser["pattern"])
        for proxy in proxies:
            try:
                ip = proxy.xpath(parser["position"]["ip"])[0].text
                port = proxy.xpath(parser["position"]["port"])[0].text
            except Exception:
                continue

            proxy = {"ip": ip, "port": port, "types": -1, "protocol": -1,
                     "country": "", "area": "", "speed": 0, "score": 0}
            proxy_list.append(proxy)
        return proxy_list

    def regular_parser(self, response, parser):
        """
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        """
        proxy_list = []
        pattern = re.compile(parser["pattern"])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser["position"]["ip"]]
                    port = match[parser["position"]["port"]]
                except Exception:
                    continue

                proxy = {"ip": ip, "port": port, "types": -1, "protocol": -1,
                         "country": "", "area": "", "speed": 0, "score": 0}
                proxy_list.append(proxy)
            return proxy_list


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