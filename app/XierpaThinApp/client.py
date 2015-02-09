# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------

from xierpathin.server.twistedmatrix.twistedclient import TwistedClient
from xierpathin.descriptors.environment import Environment

class Client(TwistedClient):

    def getSite(self, httprequest):
        site = self.app.getTheme()
        site.e = Environment(request=httprequest)
        site.e.adapter = site.adapter # Make adapter available for builders.

        # Callback to application, to allow showing request, handle form stuff, etc.
        self.app.handleRequest(httprequest, site)
        return site
