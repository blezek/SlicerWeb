
from SlicerHTTPServer import SlicerHTTPServer
from mandolin.app import app
# These are the URLs that we will respond to


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
  def start(self):
    self.logMessage ( "starting REST")
    self.server.start()
  def stop(self):
    self.logMessage ( "stopping REST")
    self.server.stop()
