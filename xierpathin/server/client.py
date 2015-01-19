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
from xierpathin.examples import Portfolio

class Client(TwistedClient):

    # Other examples to be added here as soon as they work.
    portfolio = Portfolio(title='Portfolio')
    
    THEMES = {
        # Matching theme names with Theme instances.
        TwistedClient.DEFAULTTHEME: portfolio,
        'portfolio': portfolio,  # http://localhost:8050/portfolio (same as default site)
    }
