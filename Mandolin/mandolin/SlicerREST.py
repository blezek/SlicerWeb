
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


class EchoWebSocket(WebSocket):
  def __init__(self, sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None):
    logger.debug("Initialized EchoWebSocket with socket: {}".format(sock))
    WebSocket.__init__(self,sock,protocols=protocols,extensions=extensions, environ=environ, heartbeat_freq=heartbeat_freq)
    self.sock.setblocking(False)
    self.notifier = qt.QSocketNotifier(self.sock.fileno(),qt.QSocketNotifier.Write)
    self.notifier.connect('activated(int)', self.handleWrite)
    self.write_buffer = deque()


  def once(self):
    logger.debug("Starting once")
    if self.terminated:
      logger.debug("WebSocket is already terminated")
      return False
    try:
      logger.debug("Reading data buffer from fileno: {}".format(self.sock.fileno()))
      b, foo = self.sock.recvfrom(self.reading_buffer_size)
      logger.debug("Read {}".format(b))
      if b == None:
        logger.debug ("b was None")
    except socket.error:
      logger.exception("Failed to receive data")
      return False
    else:
      logger.debug("Processing data: {} length: {}".format(b,len(b)))
      if not self.process(b):
        logger.error("Processing failed")
        return False
    logger.debug("Returning true")
    return True

  def opened(self):
    logger.info("Opened web socket {}".format(self.local_address))

  def received_message(self, message):
    """
    Automatically sends back the provided ``message`` to
    its originating endpoint.
    """
    logger.debug("EchoWebSocket.received_message {}".format(message))
    self.send(message.data, message.is_binary)

  def handleWrite(self,fd):
    logger.debug("Writing {} items".format(len(self.write_buffer)))
    while len(self.write_buffer):
      self.sock.sendall(self.write_buffer.popleft())


  def _write(self, b):
    """
    Trying to prevent a write operation
    on an already closed websocket stream.

    This cannot be bullet proof but hopefully
    will catch almost all use cases.
    """
    if self.terminated or self.sock is None:
      raise RuntimeError("Cannot send on a terminated websocket")
    self.write_buffer.append(b)

class QEchoWebSocket(WebSocket):
  def __init__(self, sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None):
    logger.debug("Initialized EchoWebSocket with socket: {}".format(sock))
    WebSocket.__init__(self,sock,protocols=protocols,extensions=extensions, environ=environ, heartbeat_freq=heartbeat_freq)
    self.sock.setblocking(False)
    self.qsock = qt.QAbstractSocket(qt.QAbstractSocket.TcpSocket, None)
    self.qsock.setSocketDescriptor(self.sock.fileno())
    self.qsock.connect('readyRead()', self.handleRead)
    self.write_buffer = deque()

  def close(self, code=1000, reason=''):
    logger.debug("QEchoWebSocket::close")

  def close_connection(self):
    logger.debug("QEchoWebSocket::close_connection")

  def terminate(self):
    logger.debug("QEchoWebSocket::close_connection")

  def once(self):
    logger.debug("Starting once")
    if self.terminated:
      logger.debug("WebSocket is already terminated")
      return False
    try:
      logger.debug("Reading data buffer from fileno: {}".format(self.sock.fileno()))
      b, foo = self.sock.recvfrom(self.reading_buffer_size)
      logger.debug("Read {}".format(b))
      if b == None:
        logger.debug ("b was None")
    except socket.error:
      logger.exception("Failed to receive data")
      return False
    else:
      logger.debug("Processing data: {} length: {}".format(b,len(b)))
      if not self.process(b):
        logger.error("Processing failed")
        return False
    logger.debug("Returning true")
    return True

  def opened(self, manager):
    logger.info("Opened web socket {}".format(self.local_address))
    self.manager = manager

  def received_message(self, message):
    """
    Automatically sends back the provided ``message`` to
    its originating endpoint.
    """
    logger.debug("EchoWebSocket.received_message {}".format(message))
    self.send(message.data, message.is_binary)

  def handleWrite(self,fd):
    logger.debug("Writing {} items".format(len(self.write_buffer)))
    while len(self.write_buffer):
      self.sock.sendall(self.write_buffer.popleft())

  def handleRead(self):
    logger.debug("QEchoWebSocket.handleRead")
    ws = self
    if ws and not ws.terminated:
      if not ws.once():
        logger.info("Terminating {} terminated? {}".format(ws,ws.terminated))
        if not ws.terminated:
          ws.terminate();
          logger.info("Terminating websocket {}".format(ws))
          self.qsock.disconnect('readyRead()', self.handleRead)
          self.manager.wsTerminated(self)

  def _write(self, b):
    """
    Trying to prevent a write operation
    on an already closed websocket stream.

    This cannot be bullet proof but hopefully
    will catch almost all use cases.
    """
    if self.terminated or self.sock is None:
      raise RuntimeError("Cannot send on a terminated websocket")
    self.qsock.sendall(self.write_buffer.popleft())


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
