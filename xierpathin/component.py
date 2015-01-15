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
#   component.py
#
from constants import Constants

class Component(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants

    def __init__(self, name=None, components=None):
        self.name = name or self.getClassName()
        self.components = components or []

    def getClassName(self):
        return self.__class__.__name__

    def _get_components(self):
        return self._components

    def _set_components(self, components):
        if not isinstance(components, (list, tuple)):
            components = [components]
        self._components = components

    components = property(_get_components, _set_components)

    def build(self, b):
        for component in self.components:
            component.build(b)


