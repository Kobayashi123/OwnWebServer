#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HTML書き換えプログラム：templatesディレクトリのHTMLファイルを書き換えます。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/14 (Created: 2022/12/14)'

import os

import settings


def render(template_name: str, context: dict):
    """
    HTMLファイルを読み込み、コンテキストの値で書き換えます。
    """
    template_path = os.path.join(settings.TEMPLATES_DIR, template_name)

    with open(template_path, 'r', encoding='utf-8') as a_file:
        template = a_file.read()

    return template.format(**context)
