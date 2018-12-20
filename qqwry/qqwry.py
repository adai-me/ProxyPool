#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-18

import os
import zlib
from struct import unpack
import requests

import socket
import codecs
import mmap

class DatDownload():
    def __init__(self):
        self.copywrite_url = "http://update.cz88.net/ip/copywrite.rar"
        self.data_url = "http://update.cz88.net/ip/qqwry.rar"

    def download(self, url, filename):
        r = requests.get(url)
        with open(filename, "wb") as code:
            code.write(r.content)

    def decipher_data(self, key, data):
        h = bytearray()
        for b in data[:0x200]:
            # b = ord(b)
            key *= 0x805
            key += 1
            key &= 0xff
            h.append(key ^ b)
        return bytes(h) + data[0x200:]

    def unpack_meta(self, data):
        (sign, version, _1, size, _, key, text, link) = unpack("<4sIIIII128s128s", data)
        sign = sign.decode("gb18030")
        text = text.rstrip(b"\x00").decode("gb18030")
        link = link.rstrip(b"\x00").decode("gb18030")
        del data
        return locals()

    def dump_dat(self, path=""):
        print("Downloading copywrite.rar")
        self.download(self.copywrite_url, path + "copywrite.rar")
        print("Downloading qqwry.rar")
        self.download(self.data_url, path + "qqwry.rar")

        print("Dumping...")
        with open(path + "copywrite.rar", "rb") as f:
            info = self.unpack_meta(f.read())

        with open(path + "qqwry.rar", "rb") as f:
            decipher = self.decipher_data(info["key"], f.read())
            dat = zlib.decompress(decipher)

        with open(path + "qqwry.dat", "wb") as f:
            f.write(dat)

        print("Dumped Success!")
        print("Clearing...")
        os.unlink(path + "copywrite.rar")
        os.unlink(path + "qqwry.rar")
        print("Cleared Success!")


class DatDump():
    def __init__(self):
        pass



if __name__ == "__main__":
    DatDownload().dump_dat("./data/")