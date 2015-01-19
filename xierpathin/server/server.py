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
#     server.py
#
#     Main server source example to be started for live serving of XierpaThin sites.

from client import Client
from xierpathin.constants import Constants
from xierpathin.server.twistedmatrix.twistedserver import TwistedServer

class Server(TwistedServer):
    pass

if __name__ == '__main__':
    client = Client()
    if Constants.USE_ONLINE:
        port = 80
    else:
        port = 8080 # Use port = 80 for serving under main domain names.
    Server().start(client, port)
