# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#    WayFinding App
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    XierpaThinAppDelegate.py
#

from AppKit import NSObject
from PyObjCTools import AppHelper

from client import Client
from twisted.internet import reactor
from twisted.web import server
from xierpathinapp import PortfolioApp

class XierpaThinAppDelegate(NSObject):
    u"""
    Main delegate for WayFinding application.
    """

    def applicationShouldTerminate_(self, sender):
        if reactor.running:
            reactor.addSystemEventTrigger('after', 'shutdown', AppHelper.stopEventLoop)
            reactor.stop()
            return False
        return True

    def applicationDidFinishLaunching_(self, notification):
        client = Client()
        client.app = PortfolioApp()
        site = server.Site(client)
        reactor.interleave(AppHelper.callAfter)
        reactor.listenTCP(client.app.port, site)

