from app import app
import slicer
import json
from bottle import request, response, HTTP_CODES, static_file
import traceback
from bottle import mako_view as view, mako_template as template
from bottle import mako_template
from bottle import MakoTemplate
import mimetypes
import os
import mako

@app.route('/static/<name:path>')
def simple_static ( name ):
	return static_file('static/' + name, root=app.config['docroot'])

# Run everything through the template engine
@app.route('/template/<name:path>')
def server_static(name):
	if 'logMessage' in app.config:
		app.config['logMessage']('handling template %s' % name)
	else:
		print ('handling template %s' % name)

	# Don't run .js files through the engine
	ext = os.path.splitext(name)[-1].lower()
	if ext != '.html' :
		return static_file(name, root=app.config['docroot'])

	print "Rendering " + name
	t = MakoTemplate ( name=name, lookup=[app.config['docroot']])
	print "Configured MakoTemplate: " + str(t)
	mimetype, encoding = mimetypes.guess_type(name)
	if mimetype: 
		response.headers['Content-Type'] = mimetype
	if encoding: 
		response.headers['Content-Encoding'] = encoding
	try:
		return t.render()
	except:
		return mako.exceptions.html_error_template().render()



