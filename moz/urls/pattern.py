#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
URL処理プログラム：URLを処理します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/09 (Created: 2022/12/09)'

import re
from typing import Callable, Optional

from moz.http.request import HttpRequest
from moz.http.response import HttpResponse


class UrlPattern:
    """
    URLパターンを処理するクラス
    """
    pattern: str
    def __init__(self, pattern: str, view: Callable[[HttpRequest], HttpResponse]):
        self.pattern = pattern
        self.view = view

    def match(self, path: str) -> Optional[re.Match]:
        """
        URLパターンとパスを受け取り、正規表現でマッチするかどうかを判定する
        マッチした場合は Match オブジェクトを返し、マッチしなかった場合は None を返す
        """
        re_pattern = re.sub(r"<(.+?)>", r"(?P<\1>[^/]+)", self.pattern)
        return re.match(re_pattern, path)
