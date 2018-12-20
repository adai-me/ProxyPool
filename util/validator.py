#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-13


import requests
from config import TEST_URL
# from spider.crawl import get_header


#测试IP是否可用

class Check():
    def __init__(self):
        pass

    def live(self, proxy):
        ip = proxy["ip"]
        port = proxy["port"]
        proxies = {
            "http": "http://%s:%s" % (ip, port),
            "https": "http://%s:%s" % (ip, port)
        }

        if TEST_URL:
            url = TEST_URL
        else:
            url = "http://httpbin.org/ip"

        try:
            r = requests.get(url=url, proxies=proxies, timeout=2)
            if r.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def addr(self, proxy):
        # 淘宝API
        url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % proxy["ip"]
        print(requests.get(url).text)

    def types(self, proxy):
        pass

    # def baidu_check(self, proxy):
    #     """
    #
    #     用baidu来检测代理的类型
    #     :param: proxy
    #     :return: proxy
    #     proxy = {"ip": ip, "port": port, "type": -1 "protocol": -1,
    #                      "country": "", "area": "", "speed": 0, "score": 0}
    #     """
        # ip = proxy["ip"]
        # port = proxy["port"]
        # protocol = proxy["protocol"]
        # type = proxy["type"]
        # speed = proxy["speed"]
        # proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
        #
        # try:
        #     start = time.time()
        #     r = requests.get(url='https://www.baidu.com', headers=get_header(), timeout=TIMEOUT, proxies=proxies)
        #     # r.encoding = chardet.detect(r.content)['encoding']
        #     if r.ok:
        #         proxy["speed"] = round(time.time() - start, 2)
        #         proxy["protocol"] = 1
        #     else:
        #         proxy["speed"] = 0
        #         proxy["protocol"] = -1
        #         types = -1
        # except Exception as e:
        #     speed = -1
        #     protocol = -1
        #     types = -1
        # return protocol, types, speed

    def check(self, proxy):
        #
        if self.live(proxy):
            print("ok")



if __name__ == "__main__":
    proxy = {'ip': '118.187.58.34', 'port': "53281", 'protocol': 0, 'types': 0,
             'country': '', 'area': '', 'score': 0, 'speed': 0}
    # print(Check().check_live(proxy))
    print(Check().check(proxy))