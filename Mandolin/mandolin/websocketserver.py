
import logging
logger = logging.getLogger('slicer.websocket.server')
logger.setLevel(logging.ERROR)

from collections import deque
from __main__ import qt

import mandolin.websocket
reload ( mandolin.websocket )
from mandolin.websocket import WebSocket, EchoWebSocket


import sys
import base64
from hashlib import sha1
WS_KEY = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Version: 13\r\n'

# WebSocket-Origin: {origin}\r\n\
# WebSocket-Location: {location}\r\n'


class WebSocketServer:
  def __init__(self, port=9999, websocket_class=EchoWebSocket):
    import socket
    # self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = qt.QTcpServer()
    self.server.listen(qt.QHostAddress("0.0.0.0"),port)
    self.server.connect('newConnection()', self.handleConnect)
    self.websocket_class = websocket_class
    self.websockets = []

  def handleConnect(self):
    logger.debug("Got connection")
    socket = self.server.nextPendingConnection()
    logger.debug("Got connection from {}".format(socket.peerName()))
    WS(socket, websocket_class=self.websocket_class, websockets=self.websockets)

  def close(self):
    for ws in self.websockets:
      try:
        ws.close()
      except:
        logger.error("Failed to close websocket")
    self.server.close()
 
class WS:
  def __init__(self, socket, websocket_class=None, websockets=None):
    self.handshaken = False 
    self.data = ''
    self.header = ''
    self.sock = socket
    self.send_buffer = deque()
    self.sock.connect('readyRead()', self.handleRead)
    self.websocket_class = websocket_class
    self.websockets = websockets
 
  def close(self):
    pass

  def handleRead(self):
    tmp = self.sock.read(2048)
    logger.debug("handleRead read {} bytes".format(tmp.size()))
    if tmp.size() == 0:
      logger.debug("Got zero bytes, closing")
      self.close()
      return
    tmp = str(tmp)
    if self.handshaken == False:
      self.header += tmp
      logger.debug ( "Looking for handshake\nheader: {}".format(self.header))
      if self.header.find('\r\n\r\n') != -1:
        self.data = self.header.split('\r\n\r\n', 1)[1]
        h = self.header.split('\r\n\r\n', 1)[0]
        s = h.split("\r\n")
        self.headers = dict(item.split(": ") for item in s[1:])
        self.handshaken = True
        key = self.headers.get('Sec-WebSocket-Key')
        if key:
          ws_key = base64.b64decode(key.encode('utf-8'))
        secret = base64.b64encode(sha1(key.encode('utf-8') + WS_KEY).digest())
        logger.debug("Sending handshake back: \n\n{}".format(handshake + 'Sec-WebSocket-Accept: ' + secret + '\r\n\r\n'))
        self.sock.write(handshake + 'Sec-WebSocket-Accept: ' + secret + '\r\n\r\n')
        logger.debug("Got handshake \nheaders: {}".format(self.headers))

        logger.debug("Turning this socket over to a WebSocket")
        self.sock.disconnect('readyRead()', self.handleRead)
        import mandolin.sws
        reload ( mandolin.sws )
        from mandolin.sws import WebSocket
        ws = self.websocket_class(self.sock)
        self.websockets.append(ws)
        ws.run()
      else:
        logger.debug("Did not get full header")
    

# while True:
#     if handshaken == False:
#         header += client.recv(16)
#         if header.find('\r\n\r\n') != -1:
#             data = header.split('\r\n\r\n', 1)[1]
#             handshaken = True
#             client.send(handshake)
#     else:
#             tmp = client.recv(128)
#             data += tmp;
 
#             validated = []
 
#             msgs = data.split('\xff')
#             data = msgs.pop()
 
#             for msg in msgs:
#                 if msg[0] == '\x00':
#                     validated.append(msg[1:])
 
#             for v in validated:
#                 print v
#                 client.send('\x00' + v + '\xff')
