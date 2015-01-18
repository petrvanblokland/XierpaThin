# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#    X I E R P A  3  A P P
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    xierpathinapp.py
#
import os
import webbrowser
from AppKit import NSInformationalAlertStyle 
import constants
from constants import AppC
from vanilla import Window, Button, CheckBox, EditText, TextEditor, TextBox, PopUpButton
from vanilla.dialogs import message
from xierpa3.sites.doingbydesign.doingbydesign import DoingByDesign
from xierpa3.builders.sassbuilder import SassBuilder
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder 
from xierpa3.builders import PhpBuilder
#from xierpathin.adapters.adapter import Adapter
from xierpathin.constants import Constants
from xierpathin.toolbox.transformer import TX
from xierpathin.examples import Portfolio

class XierpaThinApp(AppC):
    u"""Implementation of a vanilla-based GUI for the Xierpa 3 environment."""

    # Get Constants->Config as class variable, so inheriting classes can redefined values.
    C = Constants 

    PORT = 8060
    URL = 'http://localhost:%d' % PORT

    # Make sure that the PHP frameworks are downloaded from the latest version in git.
    GIT_ROOT = '/'.join(TX.module2Path(constants).split('/')[:-2]) + '/../'
    PHP_SIMPLEMVC = GIT_ROOT + 'simple-mvc-framework-v2/'
    if not os.path.exists(PHP_SIMPLEMVC):
        print 'Download //github.com/simple-mvc-framework/v2 to', PHP_SIMPLEMVC
    PHP_KIRBY = GIT_ROOT + 'kirby/'
    if not os.path.exists(PHP_KIRBY):
        print 'License //kirby.com and save to', PHP_KIRBY
        
    SITE_LABELS = [
        #("Hello world", HelloWorld()),
        #("Hello world style", HelloWorldStyle()),
        #("Hello world layout", HelloWorldLayout()),
        #("Hello world pages", HelloWorldPages()),
        #("Hello world responsive", HelloWorldResponsive()),
        #("Hello world BluePrint", HelloWorldBluePrint()),
        #("Simple responsive page", SimpleResponsivePage()),
        #("One column", OneColumnSite()),
        #("One Textile Wiki article", OneArticleSite()),
        ("Portfolio", Portfolio()),
    ]
    def __init__(self):
        u"""
        Initialize the window and open it.
        """
        self.port = self.PORT

        self.w = view = Window((AppC.WINDOW_WIDTH, AppC.WINDOW_HEIGHT), "XierpaThin",
            closable=True, minSize=(200, 200), maxSize=(1600, 1000))
        siteLabels = self.getSiteLabels()
        #y = len(siteLabels)*20
        y = 10
        bo = 25 # Button offset
        view.optionalSites = PopUpButton((10, y, 150, 24), siteLabels,
            sizeStyle='small', callback=self.selectSiteCallback)
        #view.optionalSites = RadioGroup((10, 10, 150, y), siteLabels,
        #    callback=self.selectSiteCallback, sizeStyle='small')
        self.w.optionalSites.set(0)
        y = y + 32
        view.openSite = Button((10, y, 150, 20), 'Open site', callback=self.openSiteCallback, sizeStyle='small')
        y += bo
        self.w.saveSite = Button((10, y, 150, 20), 'Save HTML+CSS', callback=self.saveSiteCallback, sizeStyle='small')
        y += bo
        view.openCss = Button((10, y, 150, 20), 'Open CSS', callback=self.openCssCallback, sizeStyle='small')
        y += bo
        #view.openSass = Button((10, y, 150, 20), 'Open SASS', callback=self.openSassCallback, sizeStyle='small')
        #y += bo
        view.openDocumentation = Button((10, y, 150, 20), 'Documentation', callback=self.openDocumentationCallback, sizeStyle='small')
        y += bo
        #view.openAsPhp = Button((10, y, 150, 20), 'Open as PHP', callback=self.openAsPhpCallback, sizeStyle='small')
        #view.makeSite = Button((10, y+95, 150, 20), 'Make site', callback=self.makeSiteCallback, sizeStyle='small')
        #view.forceCss = CheckBox((180, 10, 150, 20), 'Force make CSS', sizeStyle='small', value=True)
        view.doIndent = CheckBox((180, 30, 150, 20), 'Build indents', sizeStyle='small', value=True)
        view.forceCopy = CheckBox((180, 50, 150, 20), 'Overwrite files', sizeStyle='small', value=True)
        view.isOnline = CheckBox((180, 70, 150, 20), 'Online', sizeStyle='small', value=True, callback=self.isOnlineCallback)
        view.console = EditText((10, -200, -10, -10), sizeStyle='small')
        # Path defaults
        y = 20
        view.mampRootLabel = TextBox((300, y, 100, 20), 'MAMP folder', sizeStyle='small')
        view.mampRoot = EditText((400, y, -10, 20), self.C.PATH_MAMP, sizeStyle='small')
        y += bo
        view.exampleRootLabel = TextBox((300, y, 100, 20), 'Root folder', sizeStyle='small')
        view.exampleRoot = EditText((400, y, -10, 20), self.C.PATH_EXAMPLES, sizeStyle='small') 

        view.open()

    def getView(self):
        return self.w
        
    def getSiteLabels(self):
        siteLabels = []
        for siteLabel, _ in self.SITE_LABELS:
            siteLabels.append(siteLabel)
        return siteLabels

    def isOnlineCallback(self, sender):
        u"""Set the Constants.USE_ONLINE flag."""
        view = self.getView()
        Constants.USE_ONLINE = view.isOnline.get()
        
    def runScriptCallback(self, sender):
        view = self.getView()
        src = self.BASESCRIPT + view.script.get()
        cc = compile(src, 'abc', mode='exec')
        eval(cc, {'currentSite': self.getSite()})
        #, self.getSite().__dict__)

    def selectSiteCallback(self, sender):
        pass

    def openSiteCallback(self, sender):
        self.openSiteInBrowser(self.URL)

    def updateBuilderRootPaths(self):
        view = self.getView()
        rootPath = view.exampleRoot.get()
        HtmlBuilder.ROOT_PATH = rootPath
        SassBuilder.ROOT_PATH = rootPath
        CssBuilder.ROOT_PATH = rootPath
        
    def saveSiteCallback(self, sender):
        self.updateBuilderRootPaths()
        site = self.getSite()
        site.make()
        path = self.getExampleRootPath(site)
        if path is not None:
            webbrowser.open('file:' + path)
        
    def openSiteInBrowser(self, url):
        self.updateBuilderRootPaths()
        view = self.getView()
        if view.forceCss.get():
            url += '/' + self.C.PARAM_FORCE
        # Always open url with generic /index so css/style.css will inherit the /force
        url += '/index'
        webbrowser.open(url)
    
    def openCssCallback(self, sender):
        view = self.getView()
        self.updateBuilderRootPaths()
        url = self.URL
        if view.forceCss.get():
            url += '/' + self.C.PARAM_FORCE
        webbrowser.open(url + '/css/style.css')

    def openSassCallback(self, sender):
        url = self.URL
        #os.open(url + '/css/style.scss')

    def openDocumentationCallback(self, sender):
        self.updateBuilderRootPaths()
        url = self.URL
        webbrowser.open(url + '/' + self.C.PARAM_DOCUMENTATION + '/' + self.C.PARAM_FORCE)

    def getMampRootPath(self, site):
        view = self.getView()
        root = os.path.expanduser(view.mampRoot.get()) # File root of server.
        if not root.endswith('/'):
            root += '/'
        if not os.path.exists(root):
            message(messageText='Error in MAMP path.', informativeText='The MAMP folder "%s" does not exist.' % root, 
                alertStyle=NSInformationalAlertStyle, parentWindow=view)
            return None
        return root + site.getPythonClassName().lower() + '/' 
    
    def getExampleRootPath(self, site):
        view = self.getView()
        root = os.path.expanduser(view.exampleRoot.get()) # File root of server.
        if not root.endswith('/'):
            root += '/'
        if not os.path.exists(root):
            message(messageText='Error in Examples path.', informativeText='The Examples folder "%s" does not exist.' % root, 
                alertStyle=NSInformationalAlertStyle, parentWindow=view)
            return None
        return root + site.getPythonClassName().lower() + '/' 
    
    def openAsPhpCallback(self, sender):
        u"""Save site as PHP template in MAMP area and then open it in the browser.
        This function assumes that a PHP server like MAMP is running. Otherwise the
        page will not open in the browser."""
        view = self.getView()
        forceCopy = view.forceCopy.get() # Overwrite existing framework file?
        # Get the current selected site instance.
        site = self.getSite()
        # Save the current adapter for this site in order to restore it in the end.
        # The site instance is create on startup, and we don't want to destroy
        # the original default adapter that is already there.
        saveAdapter = site.adapter 
        #site.adapter = PhpAdapter() # Create the site running with this adapter.
        rootPath = self.getMampRootPath(site)
        # Build the CSS and and PHP/HTML files in the MAMP directory.
        builder = CssBuilder()
        site.build(builder) # Build from entire site theme, not just from template. Result is stream in builder.
        # Copy the PHP framework on that position all files/directories the not yet exist.
        # Existing files will not be overwritten, unless the forceCopy flag is True.
        builder.makeDirectory(rootPath)
        builder.copyTree(self.PHP_SIMPLEMVC, rootPath, force=forceCopy)
        # Save the created output onto the framework template
        builder.save(site, root=rootPath + 'app/templates/default/')
        # Create the PhpBuilder instance that can build/modify the PHP file structure.
        builder = PhpBuilder()
        # Render the website as export file, positioned over the default PHP framework..
        site.build(builder) # Build from entire site theme, not just from template. Result is stream in builder.
        # Copy the PHP frame work and save PHP/HTML files,
        builder.save(site, root=rootPath)
        # Restore the original adapter.
        site.adapter = saveAdapter
        # Open the site in the browser
        webbrowser.open('http://localhost:8888/%s/index.php' % site.getPythonClassName().lower())
        
    def getSite(self):
        view = self.getView()
        _, site = self.SITE_LABELS[view.optionalSites.get()]
        return site

    def makeSiteCallback(self, sender):
        self.getSite().make()

    def handleRequest(self, httprequest, site):
        self.addConsole(`httprequest` + ' ' + `site.e.form`)

    def addConsole(self, s):
        view = self.getView()
        view.console.set(view.console.get() + '\n' + s)

    def getDoIndent(self):
        u"""Answer true if building output code with indent."""
        view = self.getView()
        return view.doIndent.get()

