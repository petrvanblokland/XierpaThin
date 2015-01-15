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
#   componentnavigation.py
#
from component import Component
from constants import Constants

class Navigation(Component):

    C = Constants

    def __init__(self, adapter):
        self.adapter = adapter

    def build(self, b):
        b.div(class_=self.getClassName())
        category = self.adapter.getSelectedCategory()
        b.ul()
        for article in self.adapter.selectArticlesByCategory(category):
            if article.name == category:
                continue
            b.li()
            name = article.name.replace('_', ' ')
            if article == self.adapter.selectedArticle:
                b.span(class_=self.getClassName())
                b.text(name)
                b._span()
            else: # Different from current article.
                b.a(href=article.url)
                b.text(name)
                b._a()
            b._li()
        b._ul()
        b._div()

