#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCPサーバープログラム：このサーバープログラムにより、TCP通信をを行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/11/11 (Created: 2022/11/11)'

import socket

class TCPserver:
    """
    TCP通信を行うサーバーを表すクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """

    def serve(self):
        """
        サーバーを起動する
        """
        print("=== TCPサーバーを起動します ===")

        try:
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            # server_socket.setblocking(False)

            print("=== クライアントからの接続を待機します ===")
            (client_socket, client_address) = server_socket.accept()
            print(f"=== クライアントとの接続を確立しました client_address: {client_address} ===")

            request = client_socket.recv(4096)

            with open("server_recv.txt", "wb") as f:
                f.write(request)

            with open("server_send.txt", "rb") as f:
                response = f.read()

            client_socket.send(response)

            client_socket.close()

        finally:
            print("=== TCPサーバーを停止します ===")

def main():
    """
    Pythonファイルを生成するメイン（main）プログラムです。
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """
    server = TCPserver()
    server.serve()

if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    import sys

    sys.exit(main())
