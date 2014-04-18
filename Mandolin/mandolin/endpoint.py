
from websocketserver import WebSocketServer
from websocket import CommandWebSocket
from websocket import CommandWebSocket

import logging, vtk, json
logger = logging.getLogger('slicer.endpoint')
logger.setLevel(logging.DEBUG)


class SlicerWebSocket(CommandWebSocket):
  def on_camera_move(self,data):
    pass

  def on_connection(self,data={}):
    logger.info("Connection")
    self.emit ( "hello", { "message" : "Hi from slicer"})

  def on_camera(self,data={}):
    logger.info("Camera from grater")
    camera = self.server.camera
    if camera:
      camera.SetPosition(data['position'])
      camera.SetViewUp(data['view_up'])
      camera.SetFocalPoint(data['focal_point'])

class SlicerWebSocketServer(WebSocketServer):
  def __init__(self, port=9999, websocket_class=SlicerWebSocket):
    WebSocketServer.__init__(self,port,websocket_class)
    self.cameraNode = None
    self.camera = None
    self.cameraNodeObserverTag = None
    logger.info("Started SlicerWebSocketServer")

  def broadcast(self,t,d):
    message = {}
    message['type'] = t
    message['data'] = d
    m = json.dumps(message)
    for ws in self.websockets:
      ws.send(m)

  def onCameraNodeModified(self, observer, eventid):
    """Broadcast camera changes"""
    camera = self.cameraNode
    item = {}
    item['name'] = camera.GetName()
    item['position'] = camera.GetCamera().GetPosition()
    item['view_up'] = camera.GetCamera().GetViewUp()
    item['focal_point'] = camera.GetCamera().GetFocalPoint()
    item['id'] = camera.GetID()
    self.broadcast("camera", item)
  
  def setCameraNode(self, newCameraNode):
    """Allow to set the current camera node.
    Connected to signal 'currentNodeChanged()' emitted by camera node selector."""

    #  Remove previous observer
    if self.cameraNode and self.cameraNodeObserverTag:
      self.cameraNode.RemoveObserver(self.cameraNodeObserverTag)
    if self.camera and self.cameraObserverTag:
      self.camera.RemoveObserver(self.cameraObserverTag)

    logger.debug("set new camera")
    newCamera = None  
    if newCameraNode:
      newCamera = newCameraNode.GetCamera()
      # Add CameraNode ModifiedEvent observer
      self.cameraNodeObserverTag = newCameraNode.AddObserver(vtk.vtkCommand.ModifiedEvent, self.onCameraNodeModified)
      # Add Camera ModifiedEvent observer
      self.cameraObserverTag = newCamera.AddObserver(vtk.vtkCommand.ModifiedEvent, self.onCameraNodeModified)

    self.cameraNode = newCameraNode
    self.camera = newCamera


