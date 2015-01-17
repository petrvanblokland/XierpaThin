# PyObjC application startup.
from PyObjCTools import AppHelper

# Adds Twisted server. Using specialized reactor for integrating with arbitrary
# foreign event loop, such as those you find in GUI toolkits.
from twisted.internet._threadedselect import install
reactor = install()

# We need to import all classes used in nib files before running the
# application.
import XierpaThinAppDelegate

import objc; objc.setVerbose(True)

AppHelper.runEventLoop()
