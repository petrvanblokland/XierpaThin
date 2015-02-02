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
#   componenttext.py
#
from xierpathin.components.component import Component
from xierpathin.constants import Constants

class Text(Component):

    C = Constants

    def __init__(self, text):
        self.name = self.__class__.__name__
        self.text = text

    def build(self, b):
        b.text(self.text)


