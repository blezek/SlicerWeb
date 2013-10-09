from app import app
import slicer
import json
from bottle import request, response, HTTP_CODES
import traceback

@app.get("/slicer")
def slicer():
  r = { 'status': 'running', 'request.forms': request.forms }
  return r


def run(code):
  """Run a code object within the sandbox for this console.  The
  sandbox redirects stdout and stderr to the console, and executes
  within the namespace associated with the console."""
  from cStringIO import StringIO
  import sys
  stdout = StringIO()

  oldout, olderr = sys.stdout, sys.stderr
  sys.stdout, sys.stderr = stdout, stdout
  d = {}
  try:
    exec code in d
  except:
    sys.last_type = sys.exc_type
    sys.last_value = sys.exc_value
    sys.last_traceback = sys.exc_traceback.tb_next
    traceback.print_exception(sys.last_type, sys.last_value, sys.last_traceback)

  sys.stdout, sys.stderr = oldout, olderr
  print 'Returning from run!'
  return stdout.getvalue()

@app.put('/repl')
def slicer_repl():
  if not 'code' in request.forms:
    response.status = 400
    return { 'status': 'error', 'reason': 'code not found in PUT request'}
  print 'starting REPL'
  r = {'status': 'ok'}
  r['out'] = run ( request.forms.code )
  return r