import os

from PyObjCTools import AppHelper
from AppKit import NSImage, NSBundle, NSApplication
from plistlib import readPlist
from objc import Category
from WayFindingView import WayFindingView

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

    def resourcePath(self):
        return os.path.join(os.path.dirname(__file__), "dist", "WayFinding.app", "Contents", "Resources")

if __name__ == "__main__":
    print 'WayFinding: initializing'

    #loadImages(os.path.join(os.path.dirname(__file__), "Resources", "Images"))
    #loadImages(os.path.join(os.path.dirname(__file__), "Resources", "English.lproj"))

    #from lib.doodleDelegate import DoodleAppDelegate, DoodleApplication
    from WayFindingAppDelegate import WayFindingAppDelegate

    app = NSApplication.sharedApplication()
    delegate = WayFindingAppDelegate.alloc().init()
    app.setDelegate_(delegate)

    infoDictPath = os.path.join(os.path.dirname(__file__), "dist", "WayFinding.app", "Contents", "Info.plist")
    defaultInfoDict = readPlist(infoDictPath)

    infoDict = NSBundle.mainBundle().infoDictionary()

    infoDict.update(defaultInfoDict)
    infoDict["CFBundleInfoPlistURL"] = infoDictPath

    nibPath = os.path.join(os.path.dirname(__file__), "dist", "WayFinding.app", "Contents", "Resources", "en.lproj", "MainMenu.nib")
    #print 'Starting WayfindingApp as', nibPath
    NSBundle.loadNibFile_externalNameTable_withZone_(nibPath, {}, None)

    app.activateIgnoringOtherApps_(True)

    AppHelper.runEventLoop()
