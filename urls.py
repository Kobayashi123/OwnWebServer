#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
URLプログラム：URL情報を格納します。
"""

__author__ = 'Kobayashi Shun'
__version__ = '0.0.0'
__date__ = '2022/12/18 (Created: 2022/12/05)'

import views
from moz.urls.pattern import UrlPattern


url_patterns = [
    UrlPattern("/now", views.now),
    UrlPattern("/show_request", views.show_request),
    UrlPattern("/parameters", views.parameters),
    UrlPattern("/user/<user_id>/profile", views.user_profile),
    UrlPattern("/set_cookie", views.set_cookie),
    UrlPattern("/login", views.login),
    UrlPattern("/welcome", views.welcome)
]
