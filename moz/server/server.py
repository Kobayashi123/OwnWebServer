#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Webサーバープログラム：このサーバープログラムにより、HTTP通信を行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/11/29 (Created: 2022/11/29)'

import socket

from moz.server.worker import Worker

class Server:
    """
    Webサーバーを表すクラス
    """
    def serve(self):
        print("=== Server: サーバーを起動します ===")

        try:
            server_socket = self.create_server_socket()

            # server_socket.setblocking(False)

            while True:
                print("=== Server: クライアントからの接続を待機します ===")
                (client_socket, client_address) = server_socket.accept()
                print(f"=== Server: クライアントとの接続を確立しました client_address: {client_address} ===")

                thread = Worker(client_socket, client_address)
                thread.start()

        finally:
            print("=== Server: サーバーを停止します ===")

    def create_server_socket(self) -> socket.socket:
        """
        サーバーソケットを作成する
        """
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(("localhost", 8080))
        server_socket.listen(10)

        return server_socket
