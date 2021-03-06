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
#   article.py
#
from xierpathin.constants import Constants
from xierpathin.components.component import Component

class Article(Component):

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
            b.div(class_=self.C.CLASS_ROW)
            for chapter in article.chapters:
                b.text(chapter)
                b.br()
            b._div()
            b._div()

            # Image if available
            if article.images is not None:
                for imageSrc in article.images.split(' '):
                    # One of the images in the $images list in the article.
                    b.div(class_=self.getClassName()+'_image')
                    b.img(src=imageSrc)
                    b._div()
