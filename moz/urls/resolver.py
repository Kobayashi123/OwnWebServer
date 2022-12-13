#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
URL解決プログラム：URLを解決します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/13 (Created: 2022/12/09)'

from typing import Callable

from moz.http.request import HttpRequest
from moz.http.response import HttpResponse
from moz.views.static import static
from urls import url_patterns

class UrlResolver:
    """
    URLを解決するクラス
    """
    def resolve(self, request: HttpRequest) -> Callable[[HttpRequest], HttpResponse]:
        """
        URL解決を行う
        pathにマッチするURLパターンが存在した場合は、対応するviewを返す
        存在しなかった場合は、Noneを返す
        """
        for url_pattern in url_patterns:
            match = url_pattern.match(request.path)
            if match:
                request.params.update(match.groupdict())
                return url_pattern.view

        return static
