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
from vanilla import Window, Button, CheckBox, EditText, TextBox, PopUpButton
from vanilla.dialogs import message
#from xierpathin.builders.sassbuilder import SassBuilder
#from xierpathin.builders.cssbuilder import CssBuilder
from xierpathin.builders.htmlbuilder import HtmlBuilder 
#from xierpathin.builders import PhpBuilder
#from xierpathin.adapters.adapter import Adapter
from xierpathin.constants import Constants
from xierpathin.toolbox.transformer import TX
from xierpathin.examples import Portfolio

class XierpaThinApp(AppC):
    u"""Implementation of a vanilla-based GUI for the XierpaThin environment."""

    # Get Constants->Config as class variable, so inheriting classes can redefined values.
    C = Constants 

    PORT = 8080
    URL = 'http://localhost:%d' % PORT

    # Make sure that the PHP frameworks are downloaded from the latest version in git.
    #GIT_ROOT = '/'.join(TX.module2Path(constants).split('/')[:-2]) + '/../'
    #PHP_SIMPLEMVC = GIT_ROOT + 'simple-mvc-framework-v2/'
    #if not os.path.exists(PHP_SIMPLEMVC):
    #    print 'Download //github.com/simple-mvc-framework/v2 to', PHP_SIMPLEMVC
    #PHP_KIRBY = GIT_ROOT + 'kirby/'
    #if not os.path.exists(PHP_KIRBY):
    #    print 'License //kirby.com and save to', PHP_KIRBY
        
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

        self.w = view = Window((AppC.WINDOW_WIDTH, AppC.WINDOW_HEIGHT), "XierpaThin Webserver",
            closable=True, minSize=(200, 200), maxSize=(1600, 1000))
        siteLabels = self.getSiteLabels()
        yy = y = 8
        bo = 24 # Button offset
        view.optionalSites = PopUpButton((10, y, 150, 24), siteLabels,
            sizeStyle='small', callback=self.selectSiteCallback)
        self.w.optionalSites.set(0)
        y = y + 28
        view.openSite = Button((10, y, 150, 20), 'Open site', callback=self.openSiteCallback, sizeStyle='small')
        #y += bo
        #self.w.saveSite = Button((10, y, 150, 20), 'Save HTML+CSS', callback=self.saveSiteCallback, sizeStyle='small')
        y += bo
        view.openCss = Button((10, y, 150, 20), 'View CSS', callback=self.openCssCallback, sizeStyle='small')
        y += bo
        view.editCss = Button((10, y, 150, 20), 'Edit CSS', callback=self.editCssCallback, sizeStyle='small')
        #y += bo
        #view.openSass = Button((10, y, 150, 20), 'Open SASS', callback=self.openSassCallback, sizeStyle='small')
        #y += bo
        #view.openDocumentation = Button((10, y, 150, 20), 'Documentation', callback=self.openDocumentationCallback, sizeStyle='small')
        y += bo
        #view.openAsPhp = Button((10, y, 150, 20), 'Open as PHP', callback=self.openAsPhpCallback, sizeStyle='small')
        #view.makeSite = Button((10, y+95, 150, 20), 'Make site', callback=self.makeSiteCallback, sizeStyle='small')
        #view.forceCss = CheckBox((180, 10, 150, 20), 'Force make CSS', sizeStyle='small', value=True)
        cbo = 20 # Checkbox offset
        view.doIndent = CheckBox((180, yy, 150, 20), 'Build indents', sizeStyle='small', value=True)
        view.forceCopy = CheckBox((180, yy+cbo, 150, 20), 'Overwrite files', sizeStyle='small', value=True)
        view.isOnline = CheckBox((180, yy+2*cbo, 150, 20), 'Online', sizeStyle='small', value=True, callback=self.isOnlineCallback)

        y += 6
        view.console = EditText((10, y, -10, -10), sizeStyle='small')

        # Path defaults
        y = yy+2
        view.sourceRootLabel = TextBox((300, y, 80, 20), 'Source folder', sizeStyle='small')
        view.sourceRoot = EditText((380, y, -10, 20), self.PATH_SOURCES, sizeStyle='small',
            callback=self.sourceRootCallback)
        y += bo
        view.exportRootLabel = TextBox((300, y, 80, 20), 'Export folder', sizeStyle='small')
        view.exportRoot = EditText((380, y, -10, 20), self.PATH_EXPORT, sizeStyle='small')

        y += bo
        view.updateButton = Button((380, y, 80, 20), 'Update', sizeStyle='small', callback=self.updateCallback)
        self.setSourceRoot() # Force the source root of the adapter.

        view.open()

    def getView(self):
        return self.w

    def sourceRootCallback(self, sender):
        self.setSourceRoot()

    def setSourceRoot(self):
        view = self.getView()
        site = self.getSite()
        if site is not None:
            path = os.path.expanduser(view.sourceRoot.get())
            site.adapter.setPath(path)

    def updateCallback(self, sender):
        self.setSourceRoot()

    def getSiteLabels(self):
        siteLabels = []
        for siteLabel, _ in self.SITE_LABELS:
            siteLabels.append(siteLabel)
        return siteLabels

    def isOnlineCallback(self, sender):
        u"""Set the Constants.USE_ONLINE flag."""
        view = self.getView()
        Constants.USE_ONLINE = view.isOnline.get()
        
    def selectSiteCallback(self, sender):
        pass

    def openSiteCallback(self, sender):
        self.openSiteInBrowser(self.URL)

    def updateBuilderRootPaths(self):
        view = self.getView()
        rootPath = view.sourceRoot.get()
        HtmlBuilder.ROOT_PATH = rootPath
        #SassBuilder.ROOT_PATH = rootPath
        #CssBuilder.ROOT_PATH = rootPath
        
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
        #if view.forceCss.get():
        #    url += '/' + self.C.PARAM_FORCE
        # Always open url with generic /index so css/style.css will inherit the /force
        url += '/index'
        webbrowser.open(url)

    def openCssCallback(self, sender):
        view = self.getView()
        self.updateBuilderRootPaths()
        url = self.URL
        webbrowser.open(url + self.PATH_STYLE)

    def editCssCallback(self, sender):
        view = self.getView()
        self.updateBuilderRootPaths()
        os.system('open %s' % (view.sourceRoot.get() + self.PATH_STYLE))

    def openSassCallback(self, sender):
        url = self.URL
        #os.open(url + '/css/style.scss')

    def openDocumentationCallback(self, sender):
        self.updateBuilderRootPaths()
        url = self.URL
        webbrowser.open(url + '/' + self.C.PARAM_DOCUMENTATION + '/' + self.C.PARAM_FORCE)

    def XXXgetExportRootPath(self, site):
        view = self.getView()
        root = os.path.expanduser(view.exportRoot.get()) # File root of server to export static files.
        if not root.endswith('/'):
            root += '/'
        if not os.path.exists(root):
            message(messageText='Error in export path.', informativeText='The export folder "%s" does not exist.' % root,
                alertStyle=NSInformationalAlertStyle, parentWindow=view)
            return None
        return root + site.getPythonClassName().lower() + '/' 
    
    def XXXgetSourceRootPath(self, site):
        view = self.getView()
        root = os.path.expanduser(view.sourceRoot.get()) # File root of server.
        if not root.endswith('/'):
            root += '/'
        if not os.path.exists(root):
            message(messageText='Error in Examples path.', informativeText='The Examples folder "%s" does not exist.' % root, 
                alertStyle=NSInformationalAlertStyle, parentWindow=view)
            return None
        return root + site.getPythonClassName().lower() + '/' 

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

