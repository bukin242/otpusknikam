# -*- coding: utf-8 -*-
from lxml import html
import requests


def parse_url(url, encoding='utf-8'):
    page = requests.get(url, allow_redirects=True, timeout=10)
    return html.fromstring(page.content)
