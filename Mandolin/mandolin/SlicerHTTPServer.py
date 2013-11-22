from __main__ import qt

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from  wsgiref.simple_server import WSGIServer
from  wsgiref.simple_server import WSGIRequestHandler


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
  def __init__(self, server_address=("",8070), RequestHandlerClass=WSGIRequestHandler, docroot='.', logFile=None,logMessage=None):
    HTTPServer.__init__(self,server_address, RequestHandlerClass)
    self.docroot = docroot
    self.logFile = logFile
    if logMessage:
      self.logMessage = logMessage
    self.logMessage ( "Starting Mandolin SlicerHTTPServer" )

  def onSocketNotify(self,fileno):
      # based on SocketServer.py: self.serve_forever()
      self.logMessage('got request on %d' % fileno)
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

  @classmethod
  def findFreePort(self,port=8080):
    """returns a port that is not apparently in use"""
    portFree = False
    while not portFree:
      try:
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( ( "", port ) )
      except socket.error, e:
        portFree = False
        port += 1
      finally:
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