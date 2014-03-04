from app import app
from __main__ import vtk, qt, ctk, slicer
import json, inspect, types
from bottle import static_file
import bottle

def grabObject ( node ):
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
  return list_models();

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
  items = response['mesh'] = []
  count = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLModelNode")
  for i in xrange(count):
    n = slicer.mrmlScene.GetNthNodeByClass ( i, "vtkMRMLModelNode" )
    item = get_model(n.GetID())
    if item:
      items.append ( item )
  return response


@app.route("/mrml/data/<id>")
def get_data(id):
  print "Getting data for {}".format ( id )
  import tempfile, os.path, os
  # Pull off the trailing .stl
  suffix = '.stl'
  if id.endswith ( '.vtk'):
    suffix = '.stl'
    id = id[0:-4]
  if id.endswith ( '.stl' ):
    id = id[0:-4]
  # Get the MRML node
  node = slicer.mrmlScene.GetNodeByID(id)
  if not node:
    bottle.response.status = "404 Node: " + id + " was not found"
    return bottle.response
  # Get the VTK data
  # Construct a file by id
  fd, filename = tempfile.mkstemp(suffix=suffix)
  os.close(fd)
  slicer.util.saveNode ( node, filename )
  return static_file( os.path.basename(filename), root=os.path.dirname(filename), mimetype='text/html' )

# REST endpoint
@app.route("/rest/mesh")
def rest_mesh():
  return list_models();

def get_model(id):
  n = slicer.mrmlScene.GetNodeByID(id)
  if not n:
    return None
  if n.GetHideFromEditors():
    return None
  representation = ["POINTS", "LINES", "TRIANGLES" ]
  item = grabObject ( n )
  item['name'] = n.GetName()
  item['display_visibility'] = n.GetDisplayVisibility()
  item['display_node_id'] = n.GetDisplayNodeID()
  item['id'] = n.GetID()
  item['color'] = n.GetDisplayNode().GetColor()
  item['opacity'] = n.GetDisplayNode().GetOpacity()
  item['pointsize'] = n.GetDisplayNode().GetPointSize()
  item['type'] = representation[n.GetDisplayNode().GetRepresentation()]
  return item

@app.route("/rest/mesh/<id>")
def get_model_route(id):
  n = get_model(id)
  if n == None:
    bottle.response.status = "404 Node: " + id + " was not found"
    return bottle.response
  return n


@app.put("/rest/mesh/<id>")
def update_model(id):
  print "Update model {} with data {}".format ( id, bottle.request.json )
  node = slicer.mrmlScene.GetNodeByID(id)
  if not node:
    bottle.response.status = "404 Node: " + id + " was not found"
    return bottle.response
  print "Update_model"
  json = bottl.request.json
  node.GetDisplayNode().SetColor ( json['color'] )
  node.SetDisplayVisibility( json['visibility'] )
  node.GetDisplayNode().SetOpacity ( json['opacity'] )


@app.route("/rest/cameras")
def rest_camera():
  nodes = slicer.util.getNodes('vtkMRMLCamera*')
  response = {}
  items = response['cameras'] = []
  for camera in nodes.values():
    item = grabObject ( camera.GetCamera() )
    item['name'] = camera.GetName()
    item['position'] = camera.GetCamera().GetPosition()
    item['view_up'] = camera.GetCamera().GetViewUp()
    item['focal_point'] = camera.GetCamera().GetFocalPoint()
    item['id'] = camera.GetID()
    items.append(item)
  return response

