#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Responseプログラム：レスポンス情報を格納します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/05 (Created: 2022/12/05)'

from typing import Optional


class HttpResponse:
    """
    HTTPレスポンスの情報を格納するクラスです。
    """
    status_code: int
    content_type: Optional[str]
    body: bytes

    def __init__(self, status_code: int = 200, content_type: str = '', body: bytes = b'') -> None:
        self.status_code = status_code
        self.content_type = content_type
        self.body = body
