#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCPサーバープログラム：このサーバープログラムにより、TCP通信をを行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/11/29 (Created: 2022/11/11)'

import os
import socket
import traceback
from datetime import datetime

class WebServer:
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

	def __init__(self):
		"""
		コンストラクタ
		"""

	def serve(self):
		"""
		サーバーを起動する
		"""
		print("=== サーバーを起動します ===")

		try:
			server_socket = socket.socket()
			server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			server_socket.bind(("localhost", 8080))
			server_socket.listen(10)

			# server_socket.setblocking(False)

			while True:
				print("=== クライアントからの接続を待機します ===")
				(client_socket, client_address) = server_socket.accept()
				print(f"=== クライアントとの接続を確立しました client_address: {client_address} ===")

				try:
					request = client_socket.recv(4096)

					with open("server_recv.txt", "wb") as aFile:
						aFile.write(request)

					request_line, remain = request.split(b"\r\n", maxsplit=1)
					request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

					method, path, http_version = request_line.decode().split(" ")

					relative_path = path.lstrip("/")
					static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

					try:
						with open(static_file_path, "rb") as aFile:
							response_body = aFile.read()
							response_line = "HTTP/1.1 200 OK\r\n"

					except FileNotFoundError:
						response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
						response_line = "HTTP/1.1 404 Not Found\r\n"

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

					response = (response_line + response_header + "\r\n").encode() + response_body

					client_socket.send(response)

				except Exception:
					print("=== リクエストの処理中に、エラーが発生しました ===")
					traceback.print_exc()

				finally:
					client_socket.close()

		finally:
			print("=== サーバーを停止します ===")

def main():
	"""
	Pythonファイルを生成するメイン（main）プログラムです。
	常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
	"""
	server = WebServer()
	server.serve()

if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
	import sys
	sys.exit(main())
