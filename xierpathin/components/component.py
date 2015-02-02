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
from xierpathin.constants import Constants
from xierpathin.adapters.adapter import Adapter

class Component(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants

    def __init__(self, name=None, components=None, adapter=None):
        self.name = self.title = name or self.getClassName()
        self.components = components or []
        self.adapter = adapter

    def __repr__(self):
        return '[%s name:%s]' % (self.__class__.__name__, self.name)

    def getTitle(self, path=None):
        return path or self.title

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


