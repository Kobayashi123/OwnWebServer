#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
設定プログラム：静的ファイルのルートディレクトリを設定します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/06 (Created: 2022/12/06)'

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")