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
#   slideshow.py
#
from component import Component
from xierpathin.constants import Constants

class SlideShow(Component):

    C = Constants

    ARROW_RIGHT = '&gt;'
    ARROW_LEFT = '&lt;'

    def __init__(self, adapter=None):
        self.adapter = adapter

    def build(self, b):
        b.div(class_=self.getClassName())
        category = self.adapter.getSelectedCategory()
        b.a(href="#", class_=self.getClassName()+'_next')
        self.buildArrowRight(b)
        b._a()
        b.a(href="#", class_=self.getClassName()+'_prev')
        self.buildArrowLeft(b)
        b._a()
        b.ul()
        for component in self.components:
            b.li()
            component.build(b)
            b._li()
        b._ul()
        b._div()

    def buildArrowRight(self, b):
        b.text(self.ARROW_RIGHT)

    def buildArrowLeft(self, b):
        b.text(self.ARROW_LEFT)
