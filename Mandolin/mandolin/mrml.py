from app import app
import slicer
import json

@app.route("/mrml")
def mrml():
  response = {}
  nodes = slicer.util.getNodes('*')
  for key in nodes.keys():
    node = nodes[key]
    if not node.GetHideFromEditors():
      item = {}
      response[key] = item
      item['key'] = key
      item['class'] = node.GetClassName()
      item['properties'] = {}
      for method in dir ( node ):
        if "Get" in method:
          try:
            value = method.replace ( "Get", "" )
            item['properties'][value] = getattr ( node, method )()
          except:
            pass
  return response
