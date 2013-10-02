from bottle import *

app = Bottle();

@app.route('/')
def back_to_the_future():
    return server_static("index.html")

@app.route('/<filepath:path>')
def server_static(filepath):
    app.config['logMessage']('handling static file %s' % filepath)
    return static_file(filepath, root=app.config['docroot'])

@app.route('/hello')
def hello():
    return 'Hello World'

import mrml
