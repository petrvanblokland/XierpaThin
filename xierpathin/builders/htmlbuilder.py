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
#   htmlbuilder.py
#
#   Following standard
#   https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
#
from xierpathin.builders.builder import Builder
from xmltagbuilderpart import XmlTagBuilderPart
from xierpathin.builders.htmlbuilderpart import HtmlBuilderPart
from xierpathin.toolbox.transformer import TX
from xierpathin.toolbox.stack import Stack
from xierpathin.constants import Constants
from xierpathin.components.component import Component

class HtmlBuilder(XmlTagBuilderPart, HtmlBuilderPart, Builder):
    u"""
    """
    # Used for dispatching component.build_sass, and builder.isType('html'),
    # for components that want to define builder dependent behavior. In normal
    # processing of a page, this should never happen. But it can be used to
    # select specific parts of code that should not be interpreted by other builders.
    C = Constants

    ID = C.TYPE_HTML # Also the default extension of the output format.
    EXTENSION = ID
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.

    def initialize(self):
        Builder.initialize(self)
        # XmlTagBuilderPart support
        self._tagStack = Stack() # Stack with running tags for closing and XML validation

    def getUrl(self):
        u"""Answer the url of the current page. To be implemented by inheriting classes
        that actually knows about urls. Default behavior is to do nothing."""
        return self.e.getFullUrl()

    def theme(self, component):
        pass

    def _theme(self, component):
        pass 

    def page(self, component):
        u"""
        Builds the header of an HTML document.
        Note that the inheriting PhPBuilder uses the result of this method to generate
        the header.php file, as a separate result stream.
        """
        self.docType(self.ID)
        self.html()
        self.head()
        # Title depends on selected article. Otherwise show the path, if not available.
        self.title_(component.title) # Search for the title in the component  tree
        self.ieExceptions()
        # self.supportMediaQueries() # Very slow, getting this from Google?
        self.setViewPort()
        self.buildFontLinks(component)
        self.buildCssLinks(component)
        self.ieExceptions()
        # Build required search engine info, if available in self.adapter
        self.buildMetaDescription(component)
        self.buildMetaKeyWords(component)
        
        self.link(rel="apple-touch-icon-precomposed", href="img/appletouchicon.png")
        self.buildJavascript(component)
        self.buildFavIconLinks(component)
        self._head()

        self.body()
        # Instead of calling the main self.block
        self.div(class_='page_' + component.name or component.class_ or self.C.CLASS_PAGE)
        self.comment(component.getClassName()) # Add reference  Python class name of this component

    def _page(self, component):
        u"""Build the tail of an HTML document.
        Note that the inheriting PhPBuilder uses the result of this method to generate
        the footer.php file, as a separate result stream."""
        # Instead of calling the main self._block
        self._div(comment='.page_'+(component.name or component.class_ or self.C.CLASS_PAGE))
        self._body()
        self._html()

    def buildJavascript(self, component):
        if component.style and component.style.js:
            self.jsUrl(component.style.js)

    def buildFavIconLinks(self, component):
        u"""Build the favicon link, from the result of **component.adapter.getFavIcon()**.
        If the result is **None** then ignore."""
        data = component.adapter.getFavIcon()
        if data.url is not None:
            self.output("<link type='image/x-icon' rel='icon' href='%s'></link>" % data.url)

    def buildMetaDescription(self, component):
        u"""Build the meta tag with description of the site for search engines, if available in the adapter."""
        data = component.adapter.getDescription()
        if data.text is not None:
            self.meta(name=self.C.META_DESCRIPTION, content=data.text)
            
    def buildMetaKeyWords(self, component):
        u"""Build the meta tag with keywords of the site for search engines, if available in the adapter."""
        data = component.adapter.getKeyWords()
        if data.text is not None:
            self.meta(name=self.C.META_KEYWORDS, content=data.text)
            
    def XXXcssUrl(self, css):
        if not isinstance(css, (list, tuple)):
            css = [css]
        for url in css:
            self.link(href=url, rel="stylesheet", type="text/css")

    def jsUrl(self, js):
        u"""Alternative to jQuery: http://vanilla-js.com"""
        if not isinstance(js, (tuple, list)):
            js = [js]
        for url in js:
            self.script(type="text/javascript", src=url)

    def buildCssLinks(self, component):
        u"""
        Create the CSS links inside the head. /css-<SASS_STYLENAME> defines the type of CSS output from the Sass
        compiler. The CSS parameter must be one of ['nested', 'expanded', 'compact', 'compressed']
        """
        #urlName = component.root.urlName # Get the specific URL prefix for from root of this component.
        for cssUrl in component.css: # Should always be defined, default is an empty list
            #if not cssUrl.startswith('http://'):
            #    cssUrl = '/' + urlName + cssUrl
            self.link(href=cssUrl, type="text/css", charset="UTF-8", rel="stylesheet", media="screen")

    def buildFontLinks(self, component):
        u"""Build the webfont links of they are defined in **components.fonts**.
        Ignore if **self.C.useOnline()** is **False**."""
        if self.C.USEONLINE:
            for fontUrl in component.fonts: # Should always be defined, default is an empty list
                self.link(href=fontUrl, type="text/css", charset="UTF-8", rel="stylesheet", media="screen")

    def ieExceptions(self):
        self.comment("1140px Grid styles for <= IE9")
        self.newline()
        self.text("""<!--[if lte IE 9]><link rel="stylesheet" href="/cssie/ie9.css" type="text/css" media="screen" /><![endif]-->""")
        # self.text("""<link rel="stylesheet" href="cssie/ie9.css" type="text/css" media="screen,projection" />""")
        self.newline()

    def supportMediaQueries(self):
        self.comment("""Enables media queries in some unsupported browsers""")
        self.newline()
        self.script(type="text/javascript", src="http://code.google.com/p/css3-mediaqueries-js")

    def setViewPort(self):
        self.meta(name='viewport', content='width=device-width, initial-scale=1.0')

    # B L O C K

    def block(self, component):
        """Optional space for a component to build the opening of a block.
        This does **not** automatically build a **div</div> since that is not flexible enough.
        To be redefined by inheriting builder classed. Default behavior is to do nothing, except 
        showing the **component.selector** as comment/"""
        if component.selector:
            self.tabs()
            self.div(class_=component.class_)
            self.comment(component.selector)

    def _block(self, component):
        """Allow the component to build the closing of a block.
        This does **not** automatically build a **div</div> since that is not flexible enough.
        To be redefined by inheriting builder classed. Default behavior is to do nothing, except 
        showing the **component.selector** as comment."""
        if component.selector:
            self.tabs()
            self._div(comment=component.class_)
            self.comment('%s' % component.selector)

    def linkBlock(self, component, **kwargs):
        self.a(**kwargs)

    def _linkBlock(self, component):
        self._a()

    def text(self, componentOrText, **kwargs):
        u"""
        If in **self._svgMode** output as SVG tags. Otherwise just output if plain text string.
        If it is a components, then get it’s text string.
        """
        if componentOrText is None:
            return
        if isinstance(componentOrText, basestring):
            self.output(componentOrText)
        elif isinstance(componentOrText, Component): # Otherwise it must be of type component
            if componentOrText.id:
                self.span(id=id, contentEditable=componentOrText.editable)
            self.output(componentOrText.text)
            if componentOrText.id:
                self._span()
        else: # Otherwise we don't know the object. Just let it convert to text.
            self.output(`componentOrText`)

    def image(self, component, class_=None):
        u"""
        """
        if component.style:
            width = component.style.width_html # Take explicit HTML width/height if defined in component.
            height = component.style.height_html
        else:
            width = None
            height = None
        if height is None and width is None:
            width = '100%'
        elif height is not None:
            width = None
        alt = component.alt or TX.path2Name(component.url)
        self.img(src=component.url, width_html=width, height_html=height, alt=alt,
            class_=TX.flatten2Class(class_, component.getPrefixClass()))

    def element(self, **kwargs):
        u"""Elements are used for local CSS definitions. Ignored by HTML output."""
        pass
    
    # D R A W I N G
