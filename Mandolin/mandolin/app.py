from bottle import *

app = Bottle();

# import mrml
# import repl
# import template
import mimetypes

@app.route('/')
def back_to_the_future():
    return static_file( "index.html", root=app.config['docroot'])

@app.route('/<name:path>')
def simple_static ( name ):
  print "Serving {}".format ( name )
  return static_file( name, root=app.config['docroot'])
