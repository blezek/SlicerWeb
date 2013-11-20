import os
import sys
from __main__ import vtk, qt, ctk, slicer

import select
import urlparse
import urllib
import json
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import string,time
import socket

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from mandolin.SlicerREST import SlicerREST

import numpy

# Note: this needs to be installed in slicer's python
# in order for any of the image operations to work
hasImage = True
try:
  from PIL import Image
except ImportError:
  hasImage = False

#
# WebServer logic
#
# NB:       self.notifier = qt.QSocketNotifier(self.socket.fileno(),qt.QSocketNotifier.Read)


class MandolinLogic:
  """Include a concrete subclass of SimpleHTTPServer
  that speaks slicer.
  """
  def __init__(self, logMessage=None):
    if logMessage:
      self.logMessage = logMessage
    self.server = None
    self.logFile = '/tmp/MandolinLogic.log'
    
    if 'mandolin' in dir ( slicer.modules ):
        moduleDirectory = os.path.dirname(slicer.modules.mandolin.path)
    else:
        moduleDirectory = '/Users/blezek/Projects/SlicerWeb/Mandolin'
    self.docroot = moduleDirectory + "/docroot"
    self.port = 8090 # SlicerREST.findFreePort(self.port)
    self.server = SlicerREST(docroot=self.docroot,server_address=("",self.port),logFile=self.logFile,logMessage=self.logMessage)
    self.logMessage("Configured mandolin server on port %d" % self.port)


  # def logMessage(self,*args):
  #   for arg in args:
  #     print("Logic: " + arg)

  def start(self):
    """Create the subprocess and set up a polling timer"""
    self.logMessage("Starting Mandolin server")
    self.server.start()

  def stop(self):
    if self.server:
      self.server.stop()

#
# WebServer
#

class Mandolin:
  def __init__(self, parent):
    parent.title = "Mandolin"
    parent.categories = ["Servers"]
    parent.dependencies = []
    parent.contributors = ["Steve Pieper (Isomics)", "Daniel Blezek"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """Provides an embedded web server using Mandolin for Slicer that provides a web services API for interacting with slicer.
    """
    parent.acknowledgementText = """
This work was partially funded by NIH grant 3P41RR013218.
""" # replace with organization, grant and thanks.
    self.parent = parent


#
# WebServer widget
#

class MandolinWidget:

  def __init__(self, parent=None):
    import imp, sys, os
    self.observerTags = []
    self.guiMessages = True
    self.consoleMessages = True

    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
      self.layout = self.parent.layout()
      self.setup()
      self.parent.show()
    else:
      self.parent = parent
      self.layout = parent.layout()
    filePath = slicer.modules.mandolin.path
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)

  def enter(self):
    pass
    
  def exit(self):
    pass

  def setLogging(self):
    self.consoleMessages = self.logToConsole.checked
    self.guiMessages = self.logToGUI.checked

  def setup(self):

    # reload button
    self.reloadButton = qt.QPushButton("Reload Mandolin")
    self.reloadButton.name = "WebServer Reload"
    self.reloadButton.toolTip = "Reload this module."
    self.layout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked(bool)', self.onReload)

    self.log = qt.QTextEdit()
    self.log.readOnly = True
    self.layout.addWidget(self.log)
    # self.logMessage('<p>Status: <i>Idle</i>\n')

    # log to console
    self.logToConsole = qt.QCheckBox('Log to Console')
    self.logToConsole.setChecked(self.consoleMessages)
    self.logToConsole.toolTip = "Copy log messages to the python console and parent terminal"
    self.layout.addWidget(self.logToConsole)
    self.logToConsole.connect('clicked()', self.setLogging)

    # log to GUI
    self.logToGUI = qt.QCheckBox('Log to GUI')
    self.logToGUI.setChecked(self.guiMessages)
    self.logToGUI.toolTip = "Copy log messages to the log widget"
    self.layout.addWidget(self.logToGUI)
    self.logToGUI.connect('clicked()', self.setLogging)

    # clear log button
    self.clearLogButton = qt.QPushButton("Clear Log")
    self.clearLogButton.toolTip = "Clear the log window."
    self.layout.addWidget(self.clearLogButton)
    self.clearLogButton.connect('clicked()', self.log.clear)

    # TODO: button to start/stop server
    # TODO: warning dialog on first connect
    # TODO: config option for port

    # open local connection button
    self.localConnectionButton = qt.QPushButton("Open Page")
    self.localConnectionButton.toolTip = "Open a connection to the server on the local machine."
    self.layout.addWidget(self.localConnectionButton)
    self.localConnectionButton.connect('clicked()', self.openLocalConnection)


    self.logic = MandolinLogic(logMessage=self.logMessage)
    self.logic.start()

    # Add spacer to layout
    self.layout.addStretch(1)

  def openLocalConnection(self):
    qt.QDesktopServices.openUrl(qt.QUrl('http://localhost:8080'))

  def onReload(self):
    import imp, sys, os

    try:
      self.logic.stop()
    except AttributeError:
      # can happen if logic failed to load
      pass

    filePath = slicer.modules.mandolin.path
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)

    mod = "Mandolin"
    fp = open(filePath, "r")
    globals()[mod] = imp.load_module(mod, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    import mandolin
    try:
      SlicerREST = reload ( SlicerREST )
      mandolin = reload ( mandolin )
      reload ( mandolin.mrml )
      reload ( mandolin.app )
    except:
      self.logMessage ( "Error reloading SlicerRest")

    # rebuild the widget
    # - find and hide the existing widget
    # - remove all the layout items
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='WebServer Reload')[0].parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    globals()['mandolin'] = web = globals()[mod].MandolinWidget(parent)
    web.setup()
    # web.logic.start()


  def logMessage(self,*args):
    if self.consoleMessages:
      for arg in args:
        print(arg)
    if self.guiMessages:
      for arg in args:
        self.log.insertHtml(arg)
      self.log.insertPlainText('\n')
      self.log.ensureCursorVisible()
      self.log.repaint()
      slicer.app.processEvents(qt.QEventLoop.ExcludeUserInputEvents)






