from app import app
from __main__ import vtk, qt, ctk, slicer
import json, inspect, types
from bottle import static_file


def grabObject ( node ):
  if not node.GetHideFromEditors():
    item = {}
    item['class'] = node.GetClassName()
    for method in dir ( node ):
      if "Get" in method:
        try:
          value = method.replace ( "Get", "" )
          prop = getattr ( node, method )()
          item[value] = repr( prop )
        except:
          pass
  return item

@app.route("/nodes")
def nodes():
  return mrml();

@app.route("/mrml")
def mrml():
  response = []
  nodes = slicer.util.getNodes('*')
  for key in nodes.keys():
    node = nodes[key]
    if not node.GetHideFromEditors():
      item = grabObject ( node )
      item['id'] = key
      item['name'] = key
      item['type'] = item['class']
      response.append ( item )
  final = { 'nodes':response}
  return final

@app.route("/mrml/models")
def list_models():
  response = {}
  items = response['models'] = []
  count = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLModelNode")
  for i in xrange(count):
    n = slicer.mrmlScene.GetNthNodeByClass ( i, "vtkMRMLModelNode" )
    if n.GetHideFromEditors():
      continue
    item = {}
    item['name'] = n.GetName()
    item['display_visibility'] = n.GetDisplayVisibility()
    item['display_node_id'] = n.GetDisplayNodeID()
    item['id'] = n.GetID()
    items.append ( item )
  return response

@app.route("/mrml/data/<id>")
def get_data(id="Skin.vtk"):
  import tempfile, os.path, os
  # Pull off the trailing .stl
  id = id[0:-4]
  # Get the MRML node
  node = slicer.mrmlScene.GetFirstNodeByName(id)
  if not node:
    bottle.response.status = "404 Node: " + id + " was not found"
    return bottle.response
  # Get the VTK data
  # Construct a file by id
  fd, filename = tempfile.mkstemp(suffix=".stl")
  os.close(fd)
  slicer.util.saveNode ( node, filename )
  return static_file( os.path.basename(filename), root=os.path.dirname(filename), mimetype='text/html' )

