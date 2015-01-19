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

    def XXXbuild(self, b):
        b.div(class_=self.getClassName())
        for key, article in self.adapter.articles.items():
            b.h2()
            if article.title is None:
                b.text('Warning: no title')
            else:
                b.text(article.title)
            b._h2()
            if article.poster:
                b.img(src=article.poster)
                b.br()
            b.b()
            b.text(key)
            b._b()
            b.br()
            b.text(`article.keys()`)
            b.br()
            b.text(article.url)
            b.br()
            b.text(article.name)
            b.br()
            b.text(article.category)
            b.br()


    def build(self, b):
        # Find the active category
        category = self.adapter.findActiveCategory(b.e.getFullPath())
        articleName = b.e.form['article'] or 'index'
        activeArticle = self.adapter.findActiveArticle(articleName)

        b.div(class_=self.getClassName())
        b.ul()
        for article in self.adapter.categories[category]:
            b.li()
            if activeArticle is not None and article is activeArticle:
                b.span(class_=self.getClassName())
                b.text(article.title)
                b._span()
            else: # Different from active article.
                b.a(href='/%s/article-%s/index' % (category, article.url or 'index'))
                b.text(article.title)
                b._a()
            b._li()
        b._ul()
        b._div()

