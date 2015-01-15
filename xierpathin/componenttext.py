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
import os
from component import Component
from constants import Constants
from adapter import Adapter

class Text(Component):

    C = Constants

    def __init__(self, text):
        self.text = text

    def build(self, b):
        b.text(self.text)


