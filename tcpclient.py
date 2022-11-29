#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCPクライアントプログラム：このクライアントプログラムにより、TCP通信をを行います。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/11/14 (Created: 2022/11/14)'

import socket

class TCPclient:
    """
    TCP通信を行うクライアントを表すクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """

    def request(self):
        """
        サーバーにリクエストを送信する
        """
        print("=== クライアントを起動します ===")

        try:
            # with socket.socket() as socket:
            client_socket = socket.socket()
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            print("=== サーバーと接続します ===")
            client_socket.connect(("localhost", 80))
            print("=== サーバーとの接続が完了しました ===")

            with open("server_recv.txt", "rb") as f:
                request = f.read()

            client_socket.send(request)

            response = client_socket.recv(4096)

            with open("client_recv.txt", "wb") as f:
                f.write(response)

            client_socket.close()

        finally:
            print("=== クライアントを停止します ===")

def main():
    """
    Pythonファイルを生成するメイン（main）プログラムです。
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """
    client = TCPclient()
    client.request()

if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    import sys
    sys.exit(main())
