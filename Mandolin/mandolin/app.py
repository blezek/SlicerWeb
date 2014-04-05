from bottle import *

app = Bottle();

import mrml
import mimetypes


import logging
logger = logging.getLogger('mandolin.rest.app')
logger.setLevel(logging.INFO)



@app.route('/')
def back_to_the_future():
    return static_file( "index.html", root=app.config['docroot'])

@app.route('/<name:path>')
def simple_static ( name ):
  print "Serving {}".format ( name )
  return static_file( name, root=app.config['docroot'])


from websocket import CommandWebSocket

class SlicerWebSocket(CommandWebSocket):
  def on_camera_move(self,data):
    pass

  def on_connection(self,data={}):
    logger.info("Connection")
    self.emit ( "hello", { "message" : "Hi from slicer"})