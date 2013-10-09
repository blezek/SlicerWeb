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


@app.route("/mrml")
def mrml():
  response = {}
  nodes = slicer.util.getNodes('*')
  for key in nodes.keys():
    node = nodes[key]
    if not node.GetHideFromEditors():
      item = grabObject ( node )
      item['key'] = key
      response[key] = item
  return response
