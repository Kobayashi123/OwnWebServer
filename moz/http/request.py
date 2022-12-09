#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Requestプログラム：Requestクラスに情報を格納します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/09 (Created: 2022/12/05)'

class HttpRequest:
    """
    HTTPリクエストの情報を格納するクラスです。
    """
    path: str
    method: str
    http_version: str
    headers: dict
    body: bytes
    params: dict

    def __init__(self, path: str = "", method: str = "", http_version: str = "", headers: dict = {}, body: bytes = b"", params: dict = {}) -> None:
        self.path = path
        self.method = method
        self.http_version = http_version
        self.headers = headers
        self.body = body
        self.params = params