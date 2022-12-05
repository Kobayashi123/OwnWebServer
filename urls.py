#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
URLプログラム：URL情報を格納します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/05 (Created: 2022/12/05)'

import veiws


URL_VIEW = {
    "/now": veiws.now,
    "/show_request": veiws.show_request,
    "/parameters": veiws.parameters,
    }