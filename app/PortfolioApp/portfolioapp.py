# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    wayfindingapp.py
#
from xierpathin.htmlbuilder import HtmlBuilder
from xierpathin.transformer import TX

import wayfinding
from wayfinding.website.website import Website

class WayFindingApp(object):
    u"""
    """

    PORT = 8070
    URL = 'http://localhost:%d' % PORT

    def __init__(self):
        u"""
        Initialize the window and open it.
        """
        self.port = self.PORT
        self.url = self.URL
        self.website = Website(title='Wayfinding App')

        # Update root paths
        rootPath = TX.module2Path(wayfinding)
        HtmlBuilder.ROOT_PATH = rootPath
        SassBuilder.ROOT_PATH = rootPath
        CssBuilder.ROOT_PATH = rootPath


    def getSite(self):
        return self.website

    def handleRequest(self, httprequest, site):
        #self.addConsole(`httprequest` + ' ' + `site.e.form`)
        pass

