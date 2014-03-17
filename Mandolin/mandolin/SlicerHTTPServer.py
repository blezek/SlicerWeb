from __main__ import qt

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from  wsgiref.simple_server import WSGIServer
from  wsgiref.simple_server import WSGIRequestHandler
from ws4py.manager import WebSocketManager



import logging
logger = logging.getLogger('SlicerHTTPServer')

class QuietHandler(WSGIRequestHandler):
  def log_request(*args, **kw):
    pass

#
# SlicerHTTPServer
#

class SlicerHTTPServer(WSGIServer):
  """ 
  This web server is configured to integrate with the Qt main loop
  by listenting activity on the fileno of the servers socket.
  """
  # TODO: set header so client knows that image refreshes are needed (avoid
  # using the &time=xxx trick)
  def __init__(self, server_address=("",8070), handler_class=QuietHandler, docroot='.', logFile=None,logMessage=None):
    HTTPServer.__init__(self,server_address, handler_class)
    self.docroot = docroot
    self.logFile = logFile
    if logMessage:
      self.logMessage = logMessage
    self.logMessage ( "Starting Mandolin SlicerHTTPServer" )


  def onSocketNotify(self,fileno):
      # based on SocketServer.py: self.serve_forever()
      # self.logMessage('got request on %d' % fileno)
      logger.debug('got request on %d' % fileno)      
      self._handle_request_noblock()

  def start(self):
    """start the server
    - use one thread since we are going to communicate 
    via stdin/stdout, which will get corrupted with more threads
    """
    try:
      self.logMessage('started mandolin httpserver...')
      # self.serve_forever()
      self.notifier = qt.QSocketNotifier(self.socket.fileno(),qt.QSocketNotifier.Read)
      self.notifier.connect('activated(int)', self.onSocketNotify)
      self.logMessage('Made QT to Python notification connection...')

    except KeyboardInterrupt:
      self.logMessage('KeyboardInterrupt - stopping')
      self.stop()

  def stop(self):
    self.socket.close()
    self.notifier = None

  def logMessage(self,message):
    if self.logFile:
      fp = open(self.logFile, "a")
      fp.write(message + '\n')
      fp.close()


  def initialize_websockets_manager(self):
    """
    Call thos to start the underlying websockets
    manager. Make sure to call it once your server
    is created.
    """
    # self.manager = WebSocketManager()
    # self.manager.start()
    self.notifiers = {}
    self.websockets = {}
    print ("Initialized websockets manager")

  def handle_ws_notify(self,fileno):
    logger.debug("notified on {}".format(fileno))
    ws = self.websockets[fileno]
    ws.once();

  def link_websocket_to_server(self, ws):
    """
    Call this from your WSGI handler when a websocket
    has been created.
    """
    logger.debug("Added link to a new websocket {} with fileno {}".format(ws, ws.connection()))
    # self.manager.add(ws)
    self.websockets[ws.connection().fileno()] = ws
    notifier = qt.QSocketNotifier(ws.connection().fileno(),qt.QSocketNotifier.Read)
    self.notifiers[ws.connection().fileno()] = notifier
    notifier.connect('activated(int)', self.handler_class)

  def server_close(self):
    """
    Properly initiate closing handshakes on
    all websockets when the WSGI server terminates.
    """
    if hasattr(self, 'manager'):
      self.manager.close_all()
      self.manager.stop()
      self.manager.join()
      delattr(self, 'manager')
    slWSGIServer.server_close(self)


  @classmethod
  def findFreePort(self,port=8080):
    """returns a port that is not apparently in use"""
    import socket
    portFree = False
    s = None
    while not portFree:
      try:
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( ( "", port ) )
      except socket.error, e:
        portFree = False
        port += 1
      finally:
        if s:
          s.close()
        portFree = True
    return port

def handle ( environ, start_response ):
  return app(environ, start_response)

# s = SlicerHTTPServer(("",8080),WSGIRequestHandler)
# s.set_app(app)
# s.serve_forever()
# s.start()
# s.start()
