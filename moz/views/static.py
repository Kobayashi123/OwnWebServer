#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python生成プログラム：Pythonファイルを生成します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/13 (Created: 2022/12/13)'

import os
import traceback

import settings
from moz.http.request import HttpRequest
from moz.http.response import HttpResponse

def static(request: HttpRequest) -> HttpResponse:
    """
    静的ファイルからレスポンスを取得する
    """
    try:
        static_root = getattr(settings, "STATIC_ROOT")

        relative_path = request.path.lstrip("/")
        static_file_path = os.path.join(static_root, relative_path)

        with open(static_file_path, "rb") as a_file:
            response_body = a_file.read()

        content_type = ''
        return HttpResponse(status_code = 200, body = response_body, content_type = content_type)

    except FileNotFoundError:
        traceback.print_exc()
        response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
        content_type = "text/html"
        return HttpResponse(status_code = 404, body = response_body, content_type = content_type)
