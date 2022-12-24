#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
動的ページ生成プログラム：動的にHTMLファイルを生成します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/18 (Created: 2022/12/03)'

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

    return HttpResponse(body=html)

def show_request(request: HttpRequest) -> HttpResponse:
    """
    リクエストを表示する
    """
    content = {"request": request,
               "headers": pformat(request.headers),
               "body": request.body.decode("utf-8", "ignore"),
               }
    html = render("show_request.html", content)

    return HttpResponse(body=html)

def parameters(request: HttpRequest) -> HttpResponse:
    """
    POSTパラメータ を表示する
    """
    response_body = ''

    if request.method == "GET":
        response_body = "<html><body><h1>405 Method Not Allowed</h1></body></html>"
        return HttpResponse(body = response_body, status_code = 405)

    if request.method == "POST":
        content = {"params": urllib.parse.parse_qs(request.body.decode())}
        response_body = render("parameter.html", content)
        return HttpResponse(body = response_body)

    return HttpResponse(body = response_body)

def user_profile(request: HttpRequest) -> HttpResponse:
    """
    User ID を表示する
    """
    content = {"user_id": request.params["user_id"]}
    html = render("user_profile.html", content)

    return HttpResponse(body=html)

def set_cookie(request: HttpRequest) -> HttpResponse:
    """
    Cookieを設定する
    """
    return HttpResponse(headers={"Set-Cookie": "username=TARO"})

def login(request: HttpRequest) -> HttpResponse:
    """
    ログインページを表示する
    """
    if request.method == "GET":
        html = render("login.html", {})
        return HttpResponse(body = html)
    else:
        post_params = urllib.parse.parse_qs(request.body.decode())
        username = post_params["username"][0]

        headers = {"Location": "/welcome", "Set-Cookie": f"username={username}"}
        return HttpResponse(status_code=302, headers=headers)

def welcome(request: HttpRequest) -> HttpResponse:
    """
    Welcomeページを表示する
    """
    cookie_header = request.headers.get("Cookie", None)

    if not cookie_header:
        return HttpResponse(status_code = 302, headers = {"Location": "/login"})

    cookie_strings = cookie_header.split("; ")

    cookies = {}
    for cookie_string in cookie_strings:
        key, value = cookie_string.split("=")
        cookies[key] = value

    if "username" not in cookies:
        return HttpResponse(status_code = 302, headers = {"Location": "/login"})

    html = render("welcome.html", context = {"username": cookies["username"]})

    return HttpResponse(body = html)