#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-13

import re
from lxml import etree


class Parser():
    def __init__(self):
        pass

    def parser(self, response, parse):
        if parse["type"] == "xpath":
            return self.xpath_praser(response, parse)
        elif parse["type"] == "regular":
            return self.regular_parser(response, parse)
        elif parse["type"] == "module":
            return getattr(self, parse["moduleName"], None)(response, parse)
        else:
            return None

    def xpath_praser(self, response, parse):
        """
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        """
        proxy_list = []
        root = etree.HTML(response)
        proxies = root.xpath(parse["pattern"])
        for proxy in proxies:
            try:
                ip = proxy.xpath(parse["position"]["ip"])[0].text
                port = proxy.xpath(parse["position"]["port"])[0].text
            except Exception:
                continue

            proxy = {"ip": ip, "port": port, "types": -1, "protocol": -1,
                     "country": "", "area": "", "speed": 0, "score": 0}
            proxy_list.append(proxy)
        return proxy_list

    def regular_parser(self, response, parse):
        """
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        """
        proxy_list = []
        pattern = re.compile(parse["pattern"])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parse["position"]["ip"]]
                    port = match[parse["position"]["port"]]
                except Exception:
                    continue

                proxy = {"ip": ip, "port": port, "types": -1, "protocol": -1,
                         "country": "", "area": "", "speed": 0, "score": 0}
                proxy_list.append(proxy)
            return proxy_list


def test():
    url = "https://www.kuaidaili.com/proxylist/1"
    # response = download(url)
    # parser = PARSER_LIST[0]
    # prowies = Parser().parse(response, parser)
    # print(prowies[0])
    # url = "http://ip.taobao.com/service/getIpInfo.php?ip=210.75.225.254"
    # print(requests.get(url))
    # SQLManager().drop()
    # SQLManager().create()
    # crawl(PARSER_LIST[0])


if __name__ == "__main__":
    test()