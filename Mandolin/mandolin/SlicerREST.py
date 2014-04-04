
from SlicerHTTPServer import SlicerHTTPServer
from websocketserver import WebSocketServer
from mandolin.app import app
# These are the URLs that we will respond to

from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

import logging
logger = logging.getLogger('mandolin.rest')
logger.setLevel(logging.INFO)

from collections import deque
from __main__ import qt

#
# SlicerHTTPServer
#

class SlicerREST:
  def __init__ ( self, docroot=None,server_address=("",8321), websocket_address=("",9999), logFile=None, logMessage=None):
    # super(Flask, self).__init__("slicer")
    # self.server = web.application ( urls, globals(), autoreload=False )
    self.server = SlicerHTTPServer(server_address, docroot=docroot, logFile=logFile, logMessage=logMessage)
    self.logMessage = logMessage
    self.logMessage ( "Running Mandolin")
    app.config['docroot'] = docroot
    app.config['logMessage'] = logMessage
    self.server.set_app ( app )

    # WebSockets
    self.ws_server = WebSocketServer(port=websocket_address[1])

  def start(self):
    self.logMessage ( "starting REST")
    self.server.start()
  def stop(self):
    self.logMessage ( "stopping REST")
    self.server.stop()
    self.ws_server.stop()
