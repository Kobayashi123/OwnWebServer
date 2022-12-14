#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python生成プログラム：Pythonファイルを生成します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/13 (Created: 2022/12/03)'

import textwrap
import urllib.parse
from datetime import datetime
from pprint import pformat

from moz.http.request import HttpRequest
from moz.http.response import HttpResponse
from moz.templates.renderer import render


def now(request: HttpRequest) -> HttpResponse:
    """
    現在時刻を取得するHTMLを生成する
    """
    context = {"now": datetime.now()}

    html = render("now.html", context)

    response_body = textwrap.dedent(html).encode()
    content_type = "text/html; charset=utf-8"

    return HttpResponse(body=response_body, content_type=content_type, status_code=200)

def show_request(request: HttpRequest) -> HttpResponse:
    """
    リクエストを表示する
    """
    html = f"""\
            <html>
            <body>
                <h1>Request Line: </h1>
                <p>{request.method} {request.path} {request.http_version}</p>
                <h1>Headers: </h1>
                <pre>{pformat(request.headers)}</pre>
                <h1>Body: </h1>
                <pre>{request.body.decode("utf-8", "ignore")}</pre>
            </body>
            </html>
            """
    response_body = textwrap.dedent(html).encode()
    content_type = "text/html; charset=utf-8"

    return HttpResponse(body=response_body, content_type=content_type, status_code=200)

def parameters(request: HttpRequest) -> HttpResponse:
    """
    POSTパラメータ を表示する
    """
    response_body = b''
    content_type = ''
    status_code = 200

    if request.method == "GET":
        response_body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        content_type = "text/html; charset=utf-8"
        status_code = 405

    elif request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        html = f"""\
                <html>
                <body>
                    <h1>Parameters: </h1>
                    <pre>{pformat(post_params)}</pre>
                </body>
                </html>
                """
        response_body = textwrap.dedent(html).encode()
        content_type = "text/html; charset=utf-8"
        status_code = 200

    return HttpResponse(body=response_body, content_type=content_type, status_code=status_code)

def user_profile(request: HttpRequest) -> HttpResponse:
    """
    User ID を表示する
    """
    user_id = request.params["user_id"]
    html = f"""\
        <html>
        <body>
            <h1>プロフィール</h1>
            <p>ID: {user_id}</p>
        </body>
        </html>
        """
    response_body = textwrap.dedent(html).encode()
    content_type = "text/html; charset=utf-8"
    status_code = 200

    return HttpResponse(body=response_body, content_type=content_type, status_code=status_code)
