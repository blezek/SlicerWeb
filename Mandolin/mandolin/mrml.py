from app import app
from __main__ import vtk, qt, ctk, slicer
import json, inspect, types


def grabObject ( node ):
  if not node.GetHideFromEditors():
    item = {}
    item['class'] = node.GetClassName()
    item['properties'] = {}
    for method in dir ( node ):
      if "Get" in method:
        try:
          value = method.replace ( "Get", "" )
          prop = getattr ( node, method )()
          item['properties'][value] = repr( prop )
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
