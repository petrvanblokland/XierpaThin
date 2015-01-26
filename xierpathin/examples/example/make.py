
from xierpathin.adapters.adapter import Adapter
from xierpathin.builders.htmlbuilder import HtmlBuilder
from xierpathin.components.theme import Theme
from xierpathin.components.page import Page
from xierpathin.components.article import Article
from xierpathin.components.navigation import Navigation
from xierpathin.components.menu import Menu
from xierpathin.components.group import Group
from xierpathin.constants import Constants

class Example(Theme):

    # Textile: http://en.wikipedia.org/wiki/Textile_(markup_language)
    # Textile manual: http://redcloth.org/hobix.com/textile/

    C = Constants

    C.IMAGESPATH = 'SiteFormat'
    C.TITLE = 'Example Site'
    C.SOURCEROOT = '/example'
    C.EXPORTROOT = '/Applications/MAMP/htdocs'

    TITLE = 'Demo ' + C.TITLE

    def __init__(self, name=None, components=None):
        Theme.__init__(self, name=name, components=components)
        self.adapter = adapter = Adapter()
        menu = Menu(adapter)
        navigation = Navigation(adapter)
        article = Article(adapter)
        header = Group(components=(menu, navigation))
        components = (header, article)

        self.templates = (
            Page('index', title='Home', components=components),
            Page('home', title='Home', components=components),
            Page('contact', title='Contact', components=components),
        )
        # Find the categories for the menu, that actually have content.
        categories = adapter.getCategories()
        for template in self.templates:
            if template.name in categories:
                menu.addCategory(template.name)

    def make(self):
        for template in self.templates:
            for article in self.adapter.selectArticlesByCategory(template.name):
                print 'Building template', template.name, article.name
                self.adapter.select(article)
                builder = HtmlBuilder(exportRoot=self.C.EXPORTROOT)
                template.build(builder)

if __name__ == '__main__':
    example = Example()
    example.make()

