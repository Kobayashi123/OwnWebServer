#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
並列処理プログラム：このプログラムにより、並列処理を行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/5 (Created: 2022/11/11)'

import os
import re
import traceback
from datetime import datetime
from socket import socket
from threading import Thread
from typing import Tuple

import settings
from moz.http.request import HttpRequest
from moz.http.response import HttpResponse
from moz.urls.pattern import UrlPattern
from moz.urls.resolver import UrlResolver
from urls import url_patterns

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

            with open("server_recv.txt", "wb") as aFile:
                aFile.write(request_bytes)

            request = self.parse_http_request(request_bytes)

            view = UrlResolver().resolve(request)

            if view:
                response = view(request)
            else:
                try:
                    response_body = self.get_static_file_content(request.path)
                    content_type = ''
                    response = HttpResponse(status_code = 200, body = response_body, content_type = content_type)
                except FileNotFoundError:
                    traceback.print_exc()
                    response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                    content_type = "text/html"
                    response = HttpResponse(status_code = 404, body = response_body, content_type = content_type)

            response_line = self.build_response_line(response)
            response_header = self.build_response_header(response, request)
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

        return HttpRequest(method = method, path = path, http_version = http_version, headers = headers, body = request_body)

    def get_static_file_content(self, path: str) -> bytes:
        """
        リクエストから、staticファイルの内容を取得する
        """
        default_static_root = os.path.join(os.path.dirname(__file__), "../../static")
        static_root = getattr(settings, "STATIC_ROOT", default_static_root)

        relative_path = path.lstrip("/")
        static_file_path = os.path.join(settings.STATIC_ROOT, relative_path)

        with open(static_file_path, "rb") as aFile:
            return aFile.read()

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
            else:
                ext = ''
            response.content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

        response_header = ""
        response_header += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Server: Moz Server/0.1\r\n"
        response_header += f"Content-Length: {len(response.body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {response.content_type}\r\n"

        return response_header
