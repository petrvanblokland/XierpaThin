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
from xierpathin.toolbox.storage.adict import ADict
from xierpathin.lib import textile
from xierpathin.toolbox.transformer import TX

class Adapter(object):

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Constants 

    # Chapter tag, split chapters between this code.
    CHAPTER_TAG = '=C='
    # Valid$ field names
    FIELDNAMES = ('title', 'images', 'poster', 'summary', 'author', 'topic', 'categories',
        'menu', 'template', 'transfer')
    REQUIREDFIELDS = ('title', 'category')
    # Match line pattern "$fielName value"
    FIELDVALUE = re.compile('\$([\w]*) (.*)')
    # Match comma separated list
    COMMASPLIT = re.compile('[,]*[\s]*([^,]*)')

    def __init__(self, path=None):
        self.path = path # Will initialize articles if available in the path
        self.images = {} # Key is article path, value is list of image paths.
        self.menu = []
        self.categories = {}

    def _get_path(self):
        return self._path
    def _set_path(self, path):
        self._path = path
        self.categories = {} # Reset the categories
        self.articles = self._findArticles()
    path = property(_get_path, _set_path)

    def _findArticles(self, path=None, articles=None):
        if articles is None:
            articles = {}
        if path is None:
            path = self.path
        if path is not None and os.path.exists(path):
            for fileName in os.listdir(path):
                if fileName.startswith('.'):
                    continue
                filePath = path + '/' + fileName
                if os.path.isdir(filePath):
                    self._findArticles(filePath, articles)
                elif fileName == 'index.txt':
                    article = self._readArticle(filePath)
                    articles[article.url or ''] = article # If article.url not defined, it must be root
                    # Do images here too.
        # Answer list of articles.
        return articles

    def _readArticle(self, path):
        f = open(path, 'r')
        article = self._compileArticle(path, f.read())
        f.close()
        return article

    def getPosterArticles(self, category):
        posterArticles = []
        for article in self.articles.values():
            if article.poster is not None:
                if category is None or category in article.categories:
                    posterArticles.append(article)
        return posterArticles

    def getDescription(self):
        return ADict(dict(text='Adapter description'))

    def getKeyWords(self):
        return ADict(dict(text='My keyword for this site'))

    def getFavIcon(self):
        return ADict(dict(url=self.C.URL_FAVICON))

    def findActiveArticle(self, url):
        u"""Try to find the article, defined by the url. If no direct match can be found,
        (e.g. because there is no article id parameter in the url), then try to get the
        closest match. If all fails, answer None."""
        if url in self.articles:
            return self.articles[url]
        # If not found, answer the root article, so the page can use the transfer mode there.
        # The Root page/article must have key ''. Otherwise answer None.
        return self.getRootArticle()

    def getRootArticle(self):
        return self.articles.get('')

    def findSiteName(self, path):
        if path.startswith('/'):
            path = path[1:]
        return path.split('/')[0]

    def findActiveCategory(self, path):
        for name, _ in self.menu:
            if '/'+ name in path:
                return name
        # Did we find an active category
        category, _ = self.menu[0]
        return category

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

    def select(self, article):
        self.selectedArticle = article

    def getArticle(self, articleUrl):
        return self.articles.get(articleUrl)

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

    def _compileArticle(self, fullPath, wiki):
        u"""Compile the wiki text into an Article instance, but parsing the field definition, split
        on chapters and translate the chapter content through textile to html.
        See specification on :http://redcloth.org/hobix.com/textile/ """
        path = fullPath.replace(self.path, '')
        templateName = path.split('/')[1]
        articleName = path.split('/')[-2]
        url = self.path + path.replace('.txt', '.html').lower()
        article = ADict(dict(name=articleName, category=templateName, path=path, fullPath=fullPath,
            url=TX.name2UrlName(articleName)))
        text = []
        # Filter the field definitions
        wiki = wiki.replace('\r', '\n')
        for fieldName in self.FIELDNAMES:
            article[fieldName] = None
        for line in wiki.split('\n'):
            if line.startswith('$'):
                fieldName, value = self._splitFieldValue(line)
                hook = 'setField_' + fieldName
                if not fieldName in self.FIELDNAMES:
                    message = 'Illegal article parameter "%s" in article "%s".' % (fieldName, path)
                    self.editArticle(path, message)
                elif hasattr(self, hook):
                    getattr(self, hook)(value, article)
                else:
                    article[fieldName] = value
            else:
                text.append(line) # Keep normal text lines.

        # Check is all required fields are filled. Otherwise open the article file in the editor.
        for requiredField in self.REQUIREDFIELDS:
            if article[requiredField] is None:
                message = 'Missing required parameter "%s" in article "%s".' % (requiredField, path)
                self.editArticle(article.path, message)

        # Split the chapters, in the text indicated by =C=
        article.chapters = []
        for chapter in ('\n'.join(text)).split(self.CHAPTER_TAG):
            article.chapters.append(textile.textile(chapter))
        return article

    def editArticle(self, path, message=None):
        if message is not None:
            print message
        os.system('open %s' % (self.path + path))

    def setField_categories(self, line, article):
        article.categories = []
        for category in line.split(','):
            category = category.strip()
            article.categories.append(category)
            if not category in self.categories:
                self.categories[category] = []
            self.categories[category].append(article)

    def setField_menu(self, items, article):
        self.menu = []
        for menuItem in items:
            menuItem = menuItem.strip()
            menuItem = menuItem.split(':')
            if len(menuItem) == 2:
                self.menu.append(menuItem) # Tuple of (urlName, label)

