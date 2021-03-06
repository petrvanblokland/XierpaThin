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
from xierpathin.examples import Example

class Client(TwistedClient):

    # Other examples to be added here as soon as they work.
    example = Example(title='Example')

    THEMES = { # Matching theme names with Theme instances.
        TwistedClient.DEFAULTTHEME: example,
        'example': example,  # http://localhost:8050/portfolio (same as default site)
    }
