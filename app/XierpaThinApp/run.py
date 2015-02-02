import os

from PyObjCTools import AppHelper
from AppKit import NSImage, NSBundle, NSApplication
from plistlib import readPlist
from objc import Category
from XierpaThinView import XierpaThinView

_images = dict()

def loadImages(imageDir):
    for fileName in os.listdir(imageDir):
        if fileName == ".DS_Store":
            continue
        name, ext = os.path.splitext(fileName)
        if ext in [".png", ".pdf", ".icns"]:
            imagePath = os.path.join(imageDir, fileName)
            _images[name] = NSImage.alloc().initWithContentsOfFile_(imagePath)
            _images[name].setName_(name)

class NSBundle(Category(NSBundle)):
    u"""
    Loads the application bundle for breakpoint debugging.
    """

    def resourcePath(self):
        return os.path.join(os.path.dirname(__file__), "dist", "XierpaThin.app", "Contents", "Resources")

if __name__ == "__main__":
    print 'XierpaThin: initializing'

    #loadImages(os.path.join(os.path.dirname(__file__), "Resources", "Images"))
    #loadImages(os.path.join(os.path.dirname(__file__), "Resources", "English.lproj"))

    #from lib.doodleDelegate import DoodleAppDelegate, DoodleApplication
    from XierpaThinAppDelegate import XierpaThinAppDelegate

    app = NSApplication.sharedApplication()
    delegate = XierpaThinAppDelegate.alloc().init()
    app.setDelegate_(delegate)

    infoDictPath = os.path.join(os.path.dirname(__file__), "dist", "XierpaThin.app", "Contents", "Info.plist")
    defaultInfoDict = readPlist(infoDictPath)

    infoDict = NSBundle.mainBundle().infoDictionary()

    infoDict.update(defaultInfoDict)
    infoDict["CFBundleInfoPlistURL"] = infoDictPath

    nibPath = os.path.join(os.path.dirname(__file__), "dist", "XierpaThin.app", "Contents", "Resources", "en.lproj", "MainMenu.nib")
    #print 'Starting XierpaThinApp as', nibPath
    NSBundle.loadNibFile_externalNameTable_withZone_(nibPath, {}, None)

    app.activateIgnoringOtherApps_(True)

    AppHelper.runEventLoop()
