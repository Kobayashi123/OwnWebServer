#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
並列処理プログラム：このプログラムにより、並列処理を行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/24 (Created: 2022/11/11)'

import re
import traceback
from datetime import datetime
from socket import socket
from threading import Thread
from typing import Tuple

from moz.http.request import HttpRequest
from moz.http.response import HttpResponse
from moz.urls.resolver import UrlResolver

class Worker(Thread):
    """
    Webサーバーを表すクラス
    """
    MIME_TYPES = {
        "html": "text/html; charset=utf-8",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "gif": "image/gif",
        "svg": "image/svg+xml",
        "json": "application/json",
        "pdf": "application/pdf",
        "txt": "text/plain",
        "xml": "text/xml",
        }
    STATUS_LINES = {
        200: "200 OK",
        302: "302 Found",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
        }

    def __init__(self, client_socket: socket, address: Tuple[str, int]):
        """
        コンストラクタ
        """
        super().__init__()

        self.client_socket = client_socket
        self.client_address = address

    def run(self) -> None:
        """
        クライアントと接続済みのsocketを引数として受け取り、
        リクエストを処理してレスポンスを送信する
        """
        try:
            request_bytes = self.client_socket.recv(4096)

            with open("server_recv.txt", "wb") as a_file:
                a_file.write(request_bytes)

            request = self.parse_http_request(request_bytes)

            view = UrlResolver().resolve(request)

            response = view(request)

            response_line = self.build_response_line(response)
            response_header = self.build_response_header(response, request)
            if type(response.body) == str:
                response.body = response.body.encode()
            response_bytes = (response_line + response_header + "\r\n").encode() + response.body

            self.client_socket.send(response_bytes)

        except Exception:
            print("=== Worker: リクエストの処理中に、エラーが発生しました ===")
            traceback.print_exc()

        finally:
            print(f"=== Worker: クライアントとの通信を終了します client_address: {self.client_address} ===")
            self.client_socket.close()

    def parse_http_request(self, request: bytes) -> HttpRequest:
        """
        生のHTTPリクエストを、HttpRequestオブジェクトに変換する
        """
        request_line, remain = request.split(b"\r\n", maxsplit=1)
        request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

        method, path, http_version = request_line.decode().split(" ")

        headers = {}
        for header_row in request_header.decode().split("\r\n"):
            key, value = re.split(r": *", header_row, maxsplit=1)
            headers[key] = value

        cookies = {}
        if "Cookie" in headers:
            cookie_strings = headers["Cookie"].split("; ")

            for cookie_string in cookie_strings:
                key, value = cookie_string.split("=")
                cookies[key] = value

        return HttpRequest(method = method, path = path, http_version = http_version, headers = headers, cookies = cookies, body = request_body)

    def build_response_line(self, response: HttpResponse) -> str:
        """
        レスポンスラインを作成する
        """
        status_line = self.STATUS_LINES[response.status_code]
        return f"HTTP/1.1 {status_line}"

    def build_response_header(self, response: HttpResponse, request: HttpRequest) -> str:
        """
        レスポンスヘッダーを作成する
        """
        if response.content_type == '':
            if "." in request.path:
                ext = request.path.rsplit(".", maxsplit=1)[-1]
                response.content_type = self.MIME_TYPES.get(ext, "application/octet-stream")
            else:
                response.content_type = "text/html; charset=utf-8"

        response_header = ""
        response_header += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Server: Moz Server/0.1\r\n"
        response_header += f"Content-Length: {len(response.body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {response.content_type}\r\n"
        for header_name, header_value in response.headers.items():
            response_header += f"{header_name}: {header_value}\r\n"
        for cookie_name, cookie_value in response.cookies.items():
            response_header += f"Set-Cookie: {cookie_name}={cookie_value}\r\n"

        return response_header
