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
#    theme.py
#
import urllib
from vanilla.dialogs import message

from component import Component
from page import Page
from text import Text

class Theme(Component):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Component.C

    TITLE = 'Redefine cls.TITLE in inheriting theme class.'

    def __repr__(self):
        return '<Theme: %s>' % (self.name or self.TITLE)

    def reset(self):
        u"""Gets called prior to every page render. Can be redefined by inheriting theme classes.
        Default behavior is to do nothing."""
        pass

    def getMatchingTemplate(self, b):
        u"""
        Find the page template in self.components that has the best name match with currently available parameters in
        **self.e.form**. Unquote the url parameters and remove the spaces to create potential template names.
        Then match them against the available template components of **self**.
        """
        articleName = b.e.form['article'] or 'home'
        article = self.adapter.findActiveArticle(articleName)
        if article is None:
            template = self.getDefaultTemplate()
        else:
            template = self.getTemplate(article.template)
            if template is None:
                # Could not find a match, answer the default template.
                # If no default component exists, then answer self.
                # This happens if there is only one page in the site.
                template = self.getTemplate(self.C.TEMPLATE_DEFAULT) or self.getDefaultTemplate()
        return template

    def getTemplate(self, name):
        if name is None:
            name = self.C.TEMPLATE_DEFAULT
        for template in self.templates:
            if template.name.strip() == name.strip():
                return template
        return None

    def getDefaultTemplate(self):
        u"""Answer last resort template. Nothing else could be found."""
        p = Page('Default template', components=Text('No template found'))
        return p

    def buildBlock(self, builder):
        u"""Build the current page of this theme."""
        builder.theme(self) # Make the builder open the site.
        for component in self.components:
            component.build(builder) # Make all components of the theme build themselves.
        builder._theme(self) # Make the builder close the site.

    def handlePost(self):
        pass

    def getClassName(self):
        return None # Selector does not show, just the style block.

