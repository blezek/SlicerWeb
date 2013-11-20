from bottle import *

app = Bottle();

import mrml
import repl
import template
import mimetypes

@app.route('/')
def back_to_the_future():
    return server_static("index.html")

