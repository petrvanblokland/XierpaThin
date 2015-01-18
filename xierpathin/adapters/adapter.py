# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  T H I N
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#   adapter.py
#
import os
import re
from xierpathin.constants import Constants
from xierpathin.toolbox.adict import ADict
from xierpathin.lib import textile

class Adapter(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants 

    # Chapter tag, split chapters between this code.
    CHAPTER_TAG = '=C='
    # Match line pattern "$fielName value"
    FIELDVALUE = re.compile('\$([\w]*) (.*)')
    # Match comma separated list
    COMMASPLIT = re.compile('[,]*[\s]*([^,]*)')

    def __init__(self, path, sourceRoot=None):
        self.path = path
        self.sourceRoot = sourceRoot or self.C.SOURCEROOT
        self.articles = self._findArticles()
        self.images = {} # Key is article path, value is list of image paths.

    def _findArticles(self, path=None, articles=None):
        if articles is None:
            articles = {}
        if path is None:
            path = self.path
        for fileName in os.listdir(path):
            if fileName.startswith('.'):
                continue
            filePath = path + '/' + fileName
            if os.path.isdir(filePath):
                self._findArticles(filePath, articles)
            elif fileName == 'index.txt':
                articles[filePath] = self._readArticle(filePath)
                # Do images here too.
        return articles
        #[ADict(dict(url='home.html', name='Home')), ADict(dict(url='toen.html', name='Toen'))]

    def _readArticle(self, path):
        f = open(path, 'r')
        article = self._compileArticle(path, f.read())
        f.close()
        return article

    def getDescription(self):
        return ADict(dict(text='Adapter description'))

    def getKeyWords(self):
        return ADict(dict(text='My keyword for this site'))

    def getFavIcon(self):
        return ADict(dict(url=self.C.URL_FAVICON))

    def selectArticlesByCategory(self, category):
        articles = []
        for article in self.articles.values():
            if article.category == category:
                articles.append(article)
        return articles

    def getCategories(self):
        u"""Answer the set of category names that are used by articles."""
        categories = set()
        for article in self.articles.values():
            categories.add(article.category)
        return categories

    def getSelectedCategory(self):
        return self.selectedArticle.category

    def getUrlFromCategory(self, category):
        return ADict(dict(url=self.sourceRoot + '/' + category.lower() + '/index.html'))

    def select(self, article):
        self.selectedArticle = article

    def _splitFieldValue(self, line):
        u"""Split the string *line* into field name (starting with $ and ending with space)
        and string value. If the field is one of @self.COMMAFIELDS@, then the value
        must be a comma separated list. Split the string into a list of values.
        """
        found = self.FIELDVALUE.findall(line)
        if found:
            fieldName, value = found[0]
            if fieldName in self.C.ADAPTER_COMMAFIELDS:
                value = self.COMMASPLIT.findall(value)[:-1] # Split and remove last empty part
            return fieldName, value
        return None, None # No field name match on this line.

    def _compileArticle(self, path, wiki):
        u"""Compile the wiki text into an Article instance, but parsing the field definition, split
        on chapters and translate the chapter content through textile to html.
        See specification on :http://redcloth.org/hobix.com/textile/ """
        path = path.replace(self.path, '')
        templateName = path.split('/')[1]
        articleName = path.split('/')[-2]
        url = self.sourceRoot + path.replace('.txt', '.html').lower()
        article = ADict(dict(name=articleName, category=templateName, url=url))
        text = []
        # Filter the field definitions
        wiki = wiki.replace('\r', '\n')
        for line in wiki.split('\n'):
            if line.startswith('$'):
                fieldName, value = self._splitFieldValue(line)
                if fieldName is not None:
                    article[fieldName] = value
            else:
                text.append(line) # Keep normal text lines.
        # Split the chapters, in the text indicated by =C=
        article.chapters = []
        for chapter in ('\n'.join(text)).split(self.CHAPTER_TAG):
            article.chapters.append(textile.textile(chapter))
        return article


if __name__ == '__main__':
    DATAPATH = '/Volumes/Archive4T/Jasper/2015-01-Archief/Site-Data'

    adapter = Adapter(DATAPATH)
    print adapter.articles
    print adapter.selectArticlesByCategory('School')
