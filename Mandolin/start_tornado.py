import tornado.httpserver
import tornado.ioloop
from tornado.log import app_log
from tornado.iostream import IOStream

from __main__ import qt



class _IOLoopImpl(object):
  def __init__(self):
    print "init _IOLoopImpl"
    pass

  def close(self):
    print "close _IOLoopImpl"
    pass

  def register(self,fd,events):
    print "register _IOLoopImpl"
    pass

  def modify(self,fd,events):
    print "modify _IOLoopImpl"
    pass

  def unregister(self,fd):
    print "unregister _IOLoopImpl"
    pass

  def poll(self,timeout):
    print "poll _IOLoopImpl"
    return {}

class SliceIOLoop(tornado.ioloop.PollIOLoop):
  def initialize(self, **kwargs):
    super(SliceIOLoop, self).initialize(impl=_IOLoopImpl(), **kwargs)

# sl = SliceIOLoop()
# sl.initialize();
# sl.install()
# Slicer doesn't like this, so replace


def handle_request(request):
  message = "You requested %s\n" % request.uri
  request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % ( len(message), message))
  request.finish()


class SlicerTornadoServer(tornado.httpserver.HTTPServer):
  def hi(self):
    print 'hi'

  def __init__(self, request_callback):
    self.useStream = True
    tornado.httpserver.HTTPServer.__init__(self,request_callback)

  def onSocketNotify(self,fileno):
    socket = self.sockets[fileno]
    print "notified of socket: {}".format(socket.getsockname())
    try:
      connection, address = socket.accept()
    except socket.error:
      return
    print "Acceptied connection from {}".format(address)
    if not self.useStream:
      self._handle_connection(connection,address)
    else:
      try:
        stream = SlicerStream(connection, io_loop=sl, max_buffer_size=self.max_buffer_size)
        # self._handle_connection(connection,address)
        self.handle_stream(stream, address)
      except Exception,e:
        print "error in connection callback {}".format(e)
        app_log.error("Error in connection callback {}".format(e))


  def add_sockets(self, sockets):
    """Makes this server start accepting connections on the given sockets.

    The ``sockets`` parameter is a list of socket objects such as
    those returned by `~tornado.netutil.bind_sockets`.
    `add_sockets` is typically used in combination with that
    method and `tornado.process.fork_processes` to provide greater
    control over the initialization of a multi-process server.
    """
    # if len(sockets) != 1:
    #   raise Exception ('Can only handle one socket! but got {}'.format(len(sockets)))
    # self.socket = sockets[0]

    self.sockets = {}
    for socket in sockets:
      self.sockets[socket.fileno()] = socket
      print "\tStarting to listen on {}".format(socket.getsockname())
      self.notifier = qt.QSocketNotifier(socket.fileno(),qt.QSocketNotifier.Read)
      self.notifier.connect('activated(int)', self.onSocketNotify)
    print('Made QT to Python notification connection...')

  def start(self):
    print ('Starting')
    pass


class SlicerStream(IOStream):
  def _run_callback(self, callback, *args):
    try:
      callback(*args)
    except Exception:
      app_log.error("Uncaught exception, closing connection.",
        exc_info=True)
      # Close the socket on an uncaught exception from a user callback
      # (It would eventually get closed when the socket object is
      # gc'd, but we don't want to rely on gc happening before we
      # run out of file descriptors)
      self.close(exc_info=True)
      # Re-raise the exception so that IOLoop.handle_callback_exception
      # can see it and log the error
      raise
    self._maybe_add_error_listener()      


http_server = SlicerTornadoServer(handle_request)
http_server.listen(8881)

# tornado.ioloop.IOLoop.instance().start()
# http_server.start()



