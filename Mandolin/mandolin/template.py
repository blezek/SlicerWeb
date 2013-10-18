from app import app
import slicer
import json
from bottle import request, response, HTTP_CODES
import traceback
from bottle import mako_view as view, mako_template as template
from bottle import mako_template
from bottle import MakoTemplate
import mimetypes

# Run everything through the template engine
@app.route('/<name:path>')
def server_static(name):
	if 'logMessage' in app.config:
		app.config['logMessage']('handling static file %s' % name)
	else:
		print ('handling static file %s' % name)

	print "Rendering " + name
	t = MakoTemplate ( name=name, lookup=[app.config['docroot']])
	print "Configured MakoTemplate: " + str(t)
	mimetype, encoding = mimetypes.guess_type(name)
	if mimetype: 
		response.headers['Content-Type'] = mimetype
	if encoding: 
		response.headers['Content-Encoding'] = encoding
	return t.render()


	return static_file(name, root=app.config['docroot'])

