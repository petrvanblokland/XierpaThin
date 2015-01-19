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
#   componentarticle.py
#
from xierpathin.constants import Constants
from xierpathin.components.component import Component

class Article(Component):

    C = Constants

    def __init__(self, adapter):
        self.adapter = adapter

    def build(self, b):
        articleName = b.e.form['article'] or 'index'

        article = self.adapter.findActiveArticle(articleName)
        if b.e.form['edit']:
            self.adapter.editArticle(article.path)

        if article is not None:
            if 'title' in article:
                # Title of the article.
                b.div(class_=self.getClassName()+'_title')
                b.text(article.title)
                b._div()

            # Main article
            b.div(class_=self.getClassName())
            for chapter in article.chapters:
                b.text(chapter)
                b.br()
            b._div()

            # Image if available
            if article.images is not None:
                for imageSrc in article.images.split(' '):
                    # One of the images in the $images list in the article.
                    b.div(class_=self.getClassName()+'_image')
                    b.img(src=imageSrc)
                    b._div()
