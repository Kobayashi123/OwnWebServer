#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Responseプログラム：レスポンス情報を格納します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/26 (Created: 2022/12/05)'

from typing import Optional, Union, List

from moz.http.cookie import Cookie

class HttpResponse:
    """
    HTTPレスポンスの情報を格納するクラスです。
    """
    status_code: int
    headers: dict
    cookies: List[Cookie]
    content_type: Optional[str]
    body: Union[bytes, str]

    def __init__(self, status_code: int = 200, headers: dict = {}, cookies: List[Cookie] = [], content_type: str = '', body: Union[bytes, str] = b''):
        """
        HttpResponseクラスのコンストラクタです。

        Args:
            status_code (int, optional): _description_. Defaults to 200.
            headers (dict, optional): _description_. Defaults to {}.
            cookies (dict, optional): _description_. Defaults to {}.
            content_type (str, optional): _description_. Defaults to ''.
            body (Union[bytes, str], optional): _description_. Defaults to b''.
        """
        self.status_code = status_code
        self.headers = headers
        self.cookies = cookies
        self.content_type = content_type
        self.body = body
