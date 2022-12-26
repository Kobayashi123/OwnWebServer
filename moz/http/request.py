#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Requestプログラム：Requestクラスに情報を格納します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/24 (Created: 2022/12/05)'

class HttpRequest:
    """
    HTTPリクエストの情報を格納するクラスです。
    """
    path: str
    method: str
    http_version: str
    headers: dict
    cookies: dict
    body: bytes
    params: dict

    def __init__(self, path: str = "", method: str = "", http_version: str = "", headers: dict = {}, cookies = {}, body: bytes = b"", params: dict = {}):
        """
        HttpRequestクラスのコンストラクタです。

        Args:
            path (str, optional): _description_. Defaults to "".
            method (str, optional): _description_. Defaults to "".
            http_version (str, optional): _description_. Defaults to "".
            headers (dict, optional): _description_. Defaults to {}.
            cookies (dict, optional): _description_. Defaults to {}.
            body (bytes, optional): _description_. Defaults to b"".
            params (dict, optional): _description_. Defaults to {}.
        """
        self.path = path
        self.method = method
        self.http_version = http_version
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.params = params
