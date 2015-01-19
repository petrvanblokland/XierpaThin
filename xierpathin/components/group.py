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
#    group.py
#
from container import Container

class Group(Container):
    u"""The **Group** implements a group with automatic responsive behavior for groups of items.
    Defined by a range of widths, a group of items is scaled to stay on the same line. If the screen width
    changes, then then the **clear** attribute is shifted value, so the line break takes place between another 
    set of items."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Container.C
    
    def buildBlockRow(self, b):
        s = self.style
        b.div(class_=self.C.CLASS_ROW)
        for component in self.components:
            component.build(b)
        b._div(comment=self.C.CLASS_ROW)
   
