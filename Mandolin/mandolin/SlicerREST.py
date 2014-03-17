
from SlicerHTTPServer import SlicerHTTPServer
from mandolin.app import app
# These are the URLs that we will respond to

from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

import logging, sys

root = logging.getLogger()

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

logger = logging.getLogger('ws4py')
logger.setLevel(logging.DEBUG)
logger.debug("Hi from ws4py")

class EchoWebSocket(WebSocket):
  def received_message(self, message):
    """
    Automatically sends back the provided ``message`` to
    its originating endpoint.
    """
    print("EchoWebSocket.received_message {}".format(message))
    self.send(message.data, message.is_binary)

#
# SlicerHTTPServer
#

class SlicerREST:
  def __init__ ( self, docroot=None,server_address=("",8321), logFile=None, logMessage=None):
    # super(Flask, self).__init__("slicer")
    # self.server = web.application ( urls, globals(), autoreload=False )
    self.server = SlicerHTTPServer(server_address, docroot=docroot, logFile=logFile, logMessage=logMessage)
    self.logMessage = logMessage
    self.logMessage ( "Running Mandolin")
    app.config['docroot'] = docroot
    app.config['logMessage'] = logMessage
    self.server.set_app ( app )

    # WebSockets
    self.ws_server = SlicerHTTPServer(("",9000), handler_class=WebSocketWSGIRequestHandler, docroot=docroot, logFile=logFile, logMessage=logMessage)
    self.ws_server.set_app(WebSocketWSGIApplication(handler_cls=EchoWebSocket))
    self.ws_server.initialize_websockets_manager()

  def start(self):
    self.logMessage ( "starting REST")
    self.server.start()
    self.ws_server.start()
  def stop(self):
    self.logMessage ( "stopping REST")
    self.server.stop()
    self.ws_server.stop()
