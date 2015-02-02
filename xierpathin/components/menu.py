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
        self.name = self.__class__.__name__
        self.adapter = adapter

    def build(self, b):
        # Find active category. If not found, it is the first of the menu.
        siteName = self.adapter.findSiteName(b.e.getFullPath())
        category = self.adapter.findActiveCategory(b.e.getFullPath())

        b.div(class_=self.getClassName())
        for name, label in self.adapter.menu:
            class_ = 'menu'
            if name == category:
                class_ += ' active'
            b.a(class_=class_, href='/%s/%s/index.html' % (siteName, name))
            b.text(label)
            b._a()
            b.text(' ')
        b._div()

