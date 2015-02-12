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
#   componentnavigation.py
#
from xierpathin.constants import Constants
from xierpathin.components.component import Component

class Navigation(Component):

    C = Constants

    def __init__(self, adapter):
        self.adapter = adapter

    def build(self, b):
        # Find the active category
        siteName = self.adapter.findSiteName(b.e.getFullPath())
        category = self.adapter.findActiveCategory(b.e.getFullPath())
        articleName = b.e.form.get('article', 'index')
        activeArticle = self.adapter.findActiveArticle(articleName)
        #print 'aaaa', siteName, articleName, category, activeArticle

        b.div(class_=self.getClassName())
        if not category in self.adapter.categories:
            b.span(style='color:red;background-color: yellow;')
            b.text('Category "%s" not defined' % category)
            b._span()
        else:
            for article in self.adapter.categories[category]:
                title = article.title #.replace(' ', '&nbsp;')
                if activeArticle is not None and article is activeArticle:
                    b.div(class_='selected')
                    b.span()
                    b.text(title)
                    b._span()
                else: # Different from active article.
                    # Add /index here to make sure that relative image URL's are on in the same folder.
                    b.div()
                    b.a(href='/%s/%s/article-%s/index.html' % (siteName, category, article.url or 'index'))
                    b.text(title)
                    b._a()
                b._div()
        b._div()

