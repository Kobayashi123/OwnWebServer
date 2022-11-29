#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
並列処理プログラム：このプログラムにより、並列処理を行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/11/29 (Created: 2022/11/11)'

import os
import textwrap
import traceback
from datetime import datetime
from socket import socket
from threading import Thread
from typing import Tuple, Optional

class WorkerThread(Thread):
	"""
	Webサーバーを表すクラス
	"""
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	STATIC_ROOT = os.path.join(BASE_DIR, "static")
	MIME_TYPES = {
		"html": "text/html",
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
			request = self.client_socket.recv(4096)

			with open("server_recv.txt", "wb") as aFile:
				aFile.write(request)

			method, path, http_version, request_header, request_body = self.parse_http_request(request)

			response_body: bytes
			response_type: Optional[str]
			response_line: str

			if path == "/now":
				html = f"""\
						<html>
						<body>
							<h1>Now: {datetime.now()}</h1>
						</body>
						</html>
						"""
				response_body = textwrap.dedent(html).encode()
				content_type = "text/html"
				response_line = "HTTP/1.1 200 OK\r\n"

			else:
				try:
					response_body = self.get_static_file_content(path)
					content_type = None
					response_line = "HTTP/1.1 200 OK\r\n"

				except FileNotFoundError:
					traceback.print_exc()
					response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
					content_type = "text/html"
					response_line = "HTTP/1.1 404 Not Found\r\n"

			response_header = self.build_response_header(path, response_body, content_type)
			response = (response_line + response_header + "\r\n").encode() + response_body

			self.client_socket.send(response)

		except Exception:
			print("=== Worker: リクエストの処理中に、エラーが発生しました ===")
			traceback.print_exc()

		finally:
			print(f"=== Worker: クライアントとの通信を終了します client_address: {self.client_address} ===")
			self.client_socket.close()

	def parse_http_request(self, request: bytes) -> tuple[str, str, str, bytes, bytes]:
		"""
		HTTPリクエストを
		1.method: str
		2.path: str
		3.http_version: str
		4.request_header: bytes
		5.request_body: bytes
		に分割する
		"""
		request_line, remain = request.split(b"\r\n", maxsplit=1)
		request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

		method, path, http_version = request_line.decode().split(" ")

		return method, path, http_version, request_header, request_body

	def get_static_file_content(self, path: str) -> bytes:
		"""
		リクエストから、staticファイルの内容を取得する
		"""

		relative_path = path.lstrip("/")
		static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

		with open(static_file_path, "rb") as aFile:
			return aFile.read()

	def build_response_header(self, path: str, response_body: bytes, content_type: Optional[str]) -> str:
		"""
		レスポンスヘッダーを作成する
		"""
		if content_type is None:
			if "." in path:
				ext = path.rsplit(".", maxsplit=1)[-1]
			else:
				ext = ""
			content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

		response_header = ""
		response_header += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
		response_header += "Server: Moz Server/0.1\r\n"
		response_header += f"Content-Length: {len(response_body)}\r\n"
		response_header += "Connection: Close\r\n"
		response_header += f"Content-Type: {content_type}\r\n"

		return response_header

def main():
	"""
	Pythonファイルを生成するメイン（main）プログラムです。
	常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
	"""

if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
	import sys
	sys.exit(main())
