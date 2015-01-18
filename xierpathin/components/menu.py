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
#   componentmenu.py
#
from xierpathin.constants import Constants
from xierpathin.components.component import Component

class Menu(Component):

    C = Constants

    def __init__(self, adapter):
        self.adapter = adapter
        self.categories = [] # Need to be filled later, when know which categories are used.

    def build(self, b):
        b.div(class_=self.getClassName())
        for category in self.categories:
            url = self.adapter.getUrlFromCategory(category).url
            b.a(href=url)
            b.text(category)
            b._a()
            b.text(' ')
        b._div()

    def addCategory(self, name):
        print '331', name
        self.categories.append(name)
