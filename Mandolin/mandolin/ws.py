"""
import mandolin.ws
ss = None
if ss:
  ss.close()

reload(mandolin.ws); ss = mandolin.ws.WServer()
"""

import logging
logger = logging.getLogger('ws')
logger.setLevel(logging.DEBUG)

from collections import deque
from __main__ import qt

import sys

handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
WebSocket-Origin: http://localhost:8888\r\n\
WebSocket-Location: ws://localhost:9999/\r\n\r\n\
'


class WServer:
  def __init__(self):
    import socket
    self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 9999))
    sock.listen(5)
    logger.debug("Binding socket {}".format(sock.fileno()))
    self.notifier = qt.QSocketNotifier(self.sock.fileno(),qt.QSocketNotifier.Read)
    self.notifier.connect('activated(int)', self.handleConnect, type=qt.Qt.BlockingQueuedConnection )
    self.notifier.setEnabled(True)
    self.write_buffer = deque()

  def handleConnect(self,fd):
    logger.debug("Got connection")
    client, address = self.sock.accept();
    logger.debug("Got connection from {}".format(address))
    self.ws = WS(client,address)

  def close(self):
    self.ws.close();
    self.notifier.disconnect("activated(int)", self.handleConnect)
    self.sock.close()
 
class WS:
  def __init__(self, client, address):
    self.handshaken = False 
    self.data = ''
    self.header = ''
    self.sock = client
    self.address = address
    self.send_buffer = deque()
    self.rnotifier = qt.QSocketNotifier(self.sock.fileno(),qt.QSocketNotifier.Read)
    self.rnotifier.connect('activated(int)', self.handleRead)
    self.wnotifier = qt.QSocketNotifier(self.sock.fileno(),qt.QSocketNotifier.Write)
    self.wnotifier.connect('activated(int)', self.handleWrite)
 
  def close(self):
    self.rnotifier.disconnect("activated(int)", self.handleRead)
    self.wnotifier.disconnect("activated(int)", self.handleWrite)
    self.rnotifier = None
    self.wnotifier = None
    self.sock.close();

  def handleWrite(self,fd):
    logger.debug ( "Sending data: {}".format(len(self.send_buffer)))
    while len(self.send_buffer):
      self.sock.sendall(self.send_buffer.popleft())

  def handleRead(self,fd):
    tmp = self.sock.recv(128)
    logger.info("handleRead read {} bytes".format(len(tmp)))
    if len(tmp) == 0:
      logger.debug("Got zero bytes, closing")
      self.close()
      return

    if self.handshaken == False:
      logger.debug ( "Looking for handshake")
      self.header += tmp
      if self.header.find('\r\n\r\n') != -1:
        self.data = self.header.split('\r\n\r\n', 1)[1]
        self.handshaken = True
        self.send_buffer.append(handshake)
        logger.debug("Got handshake")
    else:
      self.data += tmp;
      validated = []
      msgs = self.data.split('\xff')
      self.data = msgs.pop()
      for msg in msgs:
        if msg[0] == '\x00':
          validated.append(msg[1:])
 
      for v in validated:
        logger.debug("Got message: {}".format(v))
        self.send_buffer.append('\x00' + v + '\xff')


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
