#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
動的ページ生成プログラム：動的にHTMLファイルを生成します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/26 (Created: 2022/12/03)'

import urllib.parse
from datetime import datetime
from pprint import pformat

from moz.http.request import HttpRequest
from moz.http.response import HttpResponse
from moz.http.cookie import Cookie
from moz.templates.renderer import render


def now(request: HttpRequest) -> HttpResponse:
    """
    現在時刻を取得するHTMLを生成する
    """
    context = {"now": datetime.now()}
    html = render("now.html", context)

    return HttpResponse(body=html.encode())

def show_request(request: HttpRequest) -> HttpResponse:
    """
    リクエストを表示する
    """
    content = {"request": request,
               "headers": pformat(request.headers),
               "body": request.body.decode("utf-8", "ignore"),
               }
    html = render("show_request.html", content)

    return HttpResponse(body=html.encode())

def parameters(request: HttpRequest) -> HttpResponse:
    """
    POSTパラメータ を表示する
    """
    html = ''

    if request.method == "GET":
        response_body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        return HttpResponse(body = response_body, status_code = 405)

    if request.method == "POST":
        content = {"params": urllib.parse.parse_qs(request.body.decode())}
        html = render("parameter.html", content)
        return HttpResponse(body = html.encode())

    return HttpResponse(body = html.encode())

def user_profile(request: HttpRequest) -> HttpResponse:
    """
    User ID を表示する
    """
    content = {"user_id": request.params["user_id"]}
    html = render("user_profile.html", content)

    return HttpResponse(body=html.encode())

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
        return HttpResponse(body = html.encode())
    else:
        post_params = urllib.parse.parse_qs(request.body.decode())
        username = post_params["username"][0]
        email = post_params["email"][0]

        headers = {"Location": "/welcome"}
        cookies = [
            Cookie(name="username", value=username, max_age=30),
            Cookie(name="email", value=email, max_age=30),
        ]
        return HttpResponse(status_code=302, headers=headers, cookies=cookies)

def welcome(request: HttpRequest) -> HttpResponse:
    """
    Welcomeページを表示する
    """

    if "username" not in request.cookies:
        return HttpResponse(status_code = 302, headers = {"Location": "/login"})

    username = request.cookies["username"]
    email = request.cookies["email"]
    html = render("welcome.html", context = {"username": username, "email": email})

    return HttpResponse(body = html.encode())