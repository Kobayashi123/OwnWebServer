#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
exampleプログラム：webサーバープログラムを起動するプログラムです。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/05 (Created: 2022/12/05)'

import sys

from moz.server.server import Server


def main():
    """
    Webサーバープログラムを起動するメイン（main）プログラムです。
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """
    Server().serve()

if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    sys.exit(main())
