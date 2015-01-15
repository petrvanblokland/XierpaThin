
import os
import textile
from writer import Writer

class MakePortfolio(object):

    # Textile: http://en.wikipedia.org/wiki/Textile_(markup_language)
    # Textile manual: http://redcloth.org/hobix.com/textile/

    IMAGESPATH = 'SiteFormat'
    TITLE = 'Portfolio Jasper van Blokland'

    def __init__(self):
        self.result = None

    def getImagePaths(self, path, paths=None):
        if paths is None:
            paths = {}
        for fileName in os.listdir(path):
            if fileName.startswith('.'):
                continue
            filePath = path + '/' + fileName
            if os.path.isdir(filePath):
                paths[fileName] = {}
                self.getImagePaths(filePath, paths[fileName])
            elif fileName.split('.')[-1] in ('jpg', 'jpeg', 'png', 'gif'):
                paths[fileName] = filePath
        return paths

    def make(self):
        paths = self.getImagePaths(self.IMAGESPATH)
        for page, content in paths.items():
            self.buildPage(page, content, paths)

    def buildPage(self, pageName, content, paths):
        self.result = Writer()
        self.write('<html>')
        self.buildHead(pageName)
        self.buildContent(pageName, content, paths)
        self.write('</html>')

        fileName = pageName + '.html'
        self.savePage(fileName, self.result.getValue())

    def write(self, s):
        self.result.write(s)

    def buildHead(self, pageName):
        self.write('<head>')
        self.write('<title>%s | %s</title>' % (self.TITLE, pageName))
        self.write('<link media="screen" href="style.css" type="text/css" charset="UTF-8" rel="stylesheet"/>')
        self.write('</head>')

    def buildContent(self, pageName, content, paths):
        self.buildNavigation(paths)
        self.buildImageNavigation(content)
        self.buildPageText(pageName)
        for imageName, path in sorted(content.items()):
            self.write('<div class="image">')
            self.write('<a name="%s"/>' % imageName)
            self.write('<a href="#top">')
            self.write('<img src="%s" width="100%%"/><br/>' % path)
            self.write('</a>')
            self.buildImageCaption(pageName + '/' + imageName)
            self.write('</div>')

    def buildNavigation(self, paths):
        self.write('<ul class="pageNavigation">')
        for fileName in sorted(paths.keys()):
            self.write('<li><a href="%s.html">%s</a></li>' % (fileName, self.makeName(fileName)))
        self.write('</ul>')

    def buildImageNavigation(self, content):
        self.write('<a name="top"/>')
        self.write('<ul class="imageNavigation">')
        for imageName, imagePath in sorted(content.items()):
            self.write('<li><a href="#%s">' % imageName)
            self.write('<img class="icon" src="%s"/>' % imagePath)
            self.write('</a>')
            self.write('</li>')
        self.write('</ul>')

    def buildPageText(self, pageName):
        textPath = self.IMAGESPATH + '/' + pageName + '/index.txt'
        if os.path.exists(textPath):
            self.write('<div class="pageText">')
            f = open(textPath, 'rb')
            self.write(textile.textile(f.read()))
            f.close()
            self.write('</div>')

    def buildImageCaption(self, imagePath):
        captionPath = self.IMAGESPATH + '/' + '.'.join(imagePath.split('.')[:-1]) + '.txt'
        if os.path.exists(captionPath):
            self.write('<div class="caption">')
            f = open(captionPath, 'rb')
            self.write(textile.textile(f.read()))
            f.close()
            self.write('</div>')

    def makeName(self, name):
        return name.replace('_', ' ')

    def savePage(self, fileName, data):
        f = open(fileName, 'w')
        f.write(data)
        f.close()

if __name__ == '__main__':
    mp = MakePortfolio()
    mp.make()

