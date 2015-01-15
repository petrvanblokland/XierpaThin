# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#   page.py
#
import os
from component import Component
from constants import Constants

class Page(Component):

    C = Constants

    def __init__(self, name, adapter, title=None, components=None, fonts=None):
        self.name = name
        self.title = title
        self.adapter = adapter
        self.components = components or []
        self.fonts = fonts or []
        self.css = ['/jasper/style.css']
        self.style = None

    def build(self, b):
        b.page(self)
        for component in self.components:
            component.build(b)
        b._page(self)
        b.save(self.adapter.selectedArticle.url)

    def _get_title(self):
        return self._title or self.name #self.adapter.selectedArticle.title or self.name

    def _set_title(self, title):
        self._title = title

    title = property(_get_title, _set_title)
