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
#   featured.py
#
from xierpathin.constants import Constants
from xierpathin.components.component import Component

class Featured(Component):

    C = Constants

    def __init__(self, adapter):
        self.name = self.__class__.__name__
        self.adapter = adapter

    def build(self, b):
        articleName = b.e.form['article'] or 'home'

        article = self.adapter.findActiveArticle(articleName)
        if b.e.form['edit']:
            self.adapter.editArticle(article.path)

        if article is not None:
            # Main article
            b.div(class_=self.getClassName())
            for chapter in article.chapters[1:]:
                b.div(class_=self.C.CLASS_ROW)
                b.text(chapter)
                b._div()
            b._div()

            # Summary of the article on the side
            b.div(class_=self.getClassName()+'_side')
            b.div(class_=self.C.CLASS_ROW)
            b.text(article.chapters[0])
            b._div()
            b._div()

