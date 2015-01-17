
from xierpathin.adapter import Adapter
from xierpathin.htmlbuilder import HtmlBuilder
from xierpathin.page import Page
from xierpathin.componentarticle import Article
from xierpathin.componentnavigation import Navigation
from xierpathin.componentmenu import Menu
from xierpathin.constants import Constants
from mycomponent import MyComponent

class XierpaThin(object):

    """
    KISS = Keep It Simple, Stupid
    RTFM = Read The F***ing Manual

    Mapping the content
    Scaling Image Archive
    """
    # Textile: http://en.wikipedia.org/wiki/Textile_(markup_language)
    # Textile manual: http://redcloth.org/hobix.com/textile/

    C = Constants

    C.IMAGESPATH = 'SiteFormat'
    C.TITLE = 'XierpaThin Site'
    #DATAPATH = 'data'
    C.DATAPATH = '/Volumes/Archive4T/Jasper/2015-01-Archief/Site-Data'
    C.SITEPATH = '/jasper'
    C.EXPORTROOT = '/Applications/MAMP/htdocs'

    def __init__(self):

        self.adapter = adapter = Adapter(self.C.DATAPATH)
        menu = Menu(adapter)
        navigation = Navigation(adapter)
        article = Article(adapter)
        #myComponent = MyComponent(components=)
        components = (menu, navigation, article)

        self.templates = (
            Page('Home', adapter, components=components),
            Page('Leukst', adapter, components=components),
            Page('Laatst', adapter, components=components),
            Page('Vroeger', adapter, components=components),
            Page('Als', adapter, components=components),
            Page('School', adapter, components=components),
            Page('Toekomst', adapter, components=components),
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
    portfolio = Portfolio()
    portfolio.make()

