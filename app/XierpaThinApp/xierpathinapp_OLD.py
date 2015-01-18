# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    xierpathinapp.py
#

import xierpathin
from xierpathin.builders.htmlbuilder import HtmlBuilder
#from xierpathin.sassbuilder import SassBuilder
#from xierpathin.cssbuilder import CssBuilder
from xierpathin.toolbox.transformer import TX
#from xierpathin.website.website import Website

class XierpaThinApp(object):
    u"""
    Wraps XierpaThin client for Twisted server.
    """

    PORT = 8090
    URL = 'http://localhost:%d' % PORT

    def __init__(self):
        u"""
        Initialize the window and open it.
        """
        self.port = self.PORT
        self.url = self.URL
        #self.website = Website(title='Portfolio App')

        # Update root paths
        rootPath = TX.module2Path(xierpathin)
        HtmlBuilder.ROOT_PATH = rootPath
        #SassBuilder.ROOT_PATH = rootPath
        #CssBuilder.ROOT_PATH = rootPath

    def getSite(self):
        #return self.website
        pass

    def handleRequest(self, httprequest, site):
        #self.addConsole(`httprequest` + ' ' + `site.e.form`)
        pass

