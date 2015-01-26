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
import sys
import importlib
import webbrowser
from AppKit import NSInformationalAlertStyle 
from constants import AppC
from vanilla import Window, Button, CheckBox, EditText, TextBox, PopUpButton, List
from vanilla.dialogs import message
from xierpathin.builders.htmlbuilder import HtmlBuilder
from xierpathin.constants import Constants
from xierpathin.toolbox.vanillas.listcell import SmallTextListCell

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
        
    def getPathListDescriptor(self):
        return [
            dict(title='path',    width=700, cell=SmallTextListCell(editable=False), editable=False),
        ]

    def __init__(self):
        u"""
        Initialize the window and open it.
        """
        self.themes = {}
        self.port = self.PORT

        self.w = view = Window((AppC.WINDOW_WIDTH, AppC.WINDOW_HEIGHT), "Xierpa Webserver",
            closable=True, minSize=(200, 200), maxSize=(1600, 1000))
        yy = y = 6
        bo = 24 # Button offset
        view.selectedSite = PopUpButton((10, y, 150, 24), [], # Will be set on update,
            sizeStyle='small', callback=self.selectSiteCallback)

        y = y + 28
        view.openSite = Button((10, y, 150, 20), 'Open site', callback=self.openSiteCallback, sizeStyle='small')
        #y += bo
        #self.w.saveSite = Button((10, y, 150, 20), 'Save HTML+CSS', callback=self.saveSiteCallback, sizeStyle='small')
        y += bo
        view.openCss = Button((10, y, 150, 20), 'View CSS', callback=self.openCssCallback, sizeStyle='small')
        y += bo
        view.editCss = Button((10, y, 150, 20), 'Edit CSS', callback=self.editCssCallback, sizeStyle='small')
        y += bo
        view.editSite = Button((10, y, 150, 20), 'Edit site.py', callback=self.editSiteCallback, sizeStyle='small')
        #y += bo
        #view.openSass = Button((10, y, 150, 20), 'Open SASS', callback=self.openSassCallback, sizeStyle='small')
        #y += bo
        #view.openDocumentation = Button((10, y, 150, 20), 'Documentation', callback=self.openDocumentationCallback, sizeStyle='small')
        y += bo
        #view.openAsPhp = Button((10, y, 150, 20), 'Open as PHP', callback=self.openAsPhpCallback, sizeStyle='small')
        #view.makeSite = Button((10, y+95, 150, 20), 'Make site', callback=self.makeSiteCallback, sizeStyle='small')
        #view.forceCss = CheckBox((180, 10, 150, 20), 'Force make CSS', sizeStyle='small', value=True)
        yy += 2
        cbo = 20 # Checkbox offset
        view.doIndent = CheckBox((180, yy, 150, 20), 'Build indents', sizeStyle='small', value=True)
        view.forceCopy = CheckBox((180, yy+cbo, 150, 20), 'Overwrite files', sizeStyle='small', value=True)
        view.isOnline = CheckBox((180, yy+2*cbo, 150, 20), 'Online', sizeStyle='small', value=True, callback=self.isOnlineCallback)

        y += 6
        view.pageList = List((10, y, AppC.WINDOW_WIDTH-20, -100), [],
            #selectionCallback=self.fontListCallback,
            doubleClickCallback=self.editPageCallback,
            drawFocusRing=False,
            enableDelete=False,
            allowsMultipleSelection=False,
            allowsEmptySelection=True,
            drawHorizontalLines=True,
            showColumnTitles=False,
            columnDescriptions=self.getPathListDescriptor(),
            rowHeight=16)
        view.console = EditText((10, -90, -10, -10), sizeStyle='small')

        # Path defaults
        y = yy+2
        view.sourceRootLabel = TextBox((300, y, 50, 20), 'Source', sizeStyle='small')
        view.sourceRoot = EditText((350, y-2, -10, 20), self.PATH_SOURCES, sizeStyle='small',
            callback=self.sourceRootCallback)
        y += bo
        view.exportRootLabel = TextBox((300, y, 50, 20), 'Export', sizeStyle='small')
        view.exportRoot = EditText((350, y-2, -10, 20), self.PATH_EXPORT, sizeStyle='small')

        y += bo
        view.updateButton = Button((350, y, 70, 20), 'Update', sizeStyle='small', callback=self.updateCallback)

        # Now we filled the root path, we can find the site folders
        self.w.selectedSite.setItems(self.getSiteLabels())
        self.w.selectedSite.set(0) # Default select the first in the list
        self.setSourceRoot() # Force the source root of the adapter.
        self.updateThemes()

        self.update()
        view.open()

    def getView(self):
        return self.w

    def getSelectedSiteName(self):
        view = self.getView()
        return view.selectedSite.getItems()[view.selectedSite.get()]

    def getTheme(self, themeName=None):
        u"""Called by the server client to get the theme instance that relates to the name.
        If no name is requested, then answer the current selected site instance."""
        try:
            if themeName is None:
                themeName = self.getSelectedSiteName()
            return self.themes.get(themeName)
        except KeyError:
            return None

    def getCssPath(self):
        u"""Answer the CSS path of the current selected site."""
        view = self.getView()
        root = self.getRootPath()
        selectedSiteName = self.getSelectedSiteName() # Get the current selection
        return root + self.getSelectedSiteName() + self.PATH_STYLE

    def sourceRootCallback(self, sender):
        self.setSourceRoot()

    def setSourceRoot(self):
        view = self.getView()
        site = self.getTheme()
        if site is not None:
            root = os.path.expanduser(view.sourceRoot.get())
            if not root.endswith('/'):
                root += '/'
            site.adapter.setPath(root + self.getSelectedSiteName())

    def updateCallback(self, sender):
        u"""Update the theme instances."""
        self.updateThemes()
        self.update()

    def updateThemes(self):
        self.themes = {}
        view = self.getView()
        root = self.getRootPath()
        if root in sys.path:
            del sys.path[sys.path.index(root)]
        sys.path.append(root)
        for siteName in view.selectedSite.getItems():
            imported = importlib.import_module(siteName)
            self.themes[siteName] = imported.Site() # Make instance of site.
        print self.themes

    def update(self):
        view = self.getView()
        # Update the list of optional sites directly from the existing site folders.
        siteLabels = self.getSiteLabels() # Get the list of sites from existing folders.
        selectedSiteName = self.getSelectedSiteName() # Get the current selection
        view.selectedSite.setItems(siteLabels) # Set the new set of sites.
        if selectedSiteName in siteLabels: # If the original selection is still there, set it again.
            view.selectedSite.set(siteLabels.index(selectedSiteName))
        view.pageList.set(self.getPagePathRecords())
        # Set the site source root of the client web server.
        self.setSourceRoot()

    def getRootPath(self):
        view = self.getView()
        root = os.path.expanduser(view.sourceRoot.get())
        if not root.endswith('/'):
            root = root + '/'
        return root

    def getSiteLabels(self):
        u"""Get the names of folders in the source folder that contain a index.txt file."""
        view = self.getView()
        siteLabels = []
        root = self.getRootPath()
        if os.path.exists(root):
            for fileName in os.listdir(root):
                if fileName[0] in '._':
                    continue
                sitePath = root + fileName
                if os.path.isdir(sitePath) and os.path.exists(sitePath + '/index.txt') and \
                    os.path.exists(sitePath + '/py'):
                    siteLabels.append(fileName)
        return siteLabels

    def getPagePathRecords(self):
        u"""Answer the list of folder names that contain an index.html file."""
        view = self.getView()
        pagePaths = []
        root = self.getRootPath()
        if os.path.exists(root):
            sitePath = root + self.getSelectedSiteName() # Add the root index.txt of the site.
            pagePaths.append(dict(path=sitePath))
            if os.path.isdir(sitePath):
                self._findPagePathRecords(sitePath + '/', pagePaths)
        return pagePaths

    def _findPagePathRecords(self, path, pagePaths):
        for fileName in os.listdir(path):
            if fileName[0] in '._':
                continue
            pagePath = path + fileName
            if os.path.isdir(pagePath):
                if os.path.exists(pagePath + '/index.txt'):
                    pagePaths.append(dict(path=pagePath))
                self._findPagePathRecords(pagePath + '/', pagePaths)

    def isOnlineCallback(self, sender):
        u"""Set the Constants.USE_ONLINE flag."""
        view = self.getView()
        Constants.USE_ONLINE = view.isOnline.get()

    def selectSiteCallback(self, sender):
        self.update() # Update the list of pages for the selected site.

    def openSiteCallback(self, sender):
        self.openSiteInBrowser(self.URL)

    def updateBuilderRootPaths(self):
        view = self.getView()
        rootPath = view.sourceRoot.get()
        HtmlBuilder.ROOT_PATH = rootPath
        #SassBuilder.ROOT_PATH = rootPath
        #CssBuilder.ROOT_PATH = rootPath
        
    def XXXsaveSiteCallback(self, sender):
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
        os.system('open %s' % self.getCssPath())

    def editPageCallback(self, sender):
        view = self.getView()
        selection = view.pageList.getSelection()
        if selection:
            selectedPage = view.pageList.get()[selection[0]]['path']
            os.system('open %s' % selectedPage + '/index.txt')

    def editSiteCallback(self, sender):
        view = self.getView()
        os.system('open %s' % (view.sourceRoot.get() + '/' + self.getSelectedSiteName() + self.PATH_SITE))

    def openSassCallback(self, sender):
        url = self.URL
        #os.open(url + '/css/style.scss')

    def openDocumentationCallback(self, sender):
        self.updateBuilderRootPaths()
        url = self.URL
        webbrowser.open(url + '/' + self.C.PARAM_DOCUMENTATION + '/' + self.C.PARAM_FORCE)

    def handleRequest(self, httprequest, site):
        self.addConsole(`httprequest` + ' ' + `site.e.form`)

    def addConsole(self, s):
        view = self.getView()
        view.console.set(view.console.get() + '\n' + s)

    def getDoIndent(self):
        u"""Answer true if building output code with indent."""
        view = self.getView()
        return view.doIndent.get()

