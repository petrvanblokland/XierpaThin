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
#    container.py
#
from component import Component

class Container(Component):
    u"""The *Container* is the generic component that holds most other components on a page.
    Containers are always two-layered: a container @div@ to position on a page with a row @div@ inside
    that handles the responsive behavior of the content."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C

    def buildBlock(self, b):
        u"""Build the container-div with a row-div inside."""
        s = self.style
        b.div(class_=self.getClassName())
        for component in self.components:
            component.build(b)
        b._div(comment='.'+self.getClassName()) # Comment the class at end of container

