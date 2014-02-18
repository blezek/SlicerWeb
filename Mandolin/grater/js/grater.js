
 
  require(["jquery", 'foundation'], function(jquery) {
     jquery(document).foundation();
  })

require(["model", "xtk", "dat.gui"], function(model) {
// include all used X-classes here
  // this is only required when using the xtk-deps.js file
/*
  goog.require('X.renderer3D');
  goog.require('X.cube');
  goog.require('X.mesh');
*/


  meshCollection = new model.MeshCollection();
  setInterval ( function() { meshCollection.fetch() }, 2000 );


  render = new X.renderer3D();
  render.container = "render"
  render.init();

  // create a cube
  var cube = new X.cube();
  
  // setting the edge length can also be skipped since 20 is the default
  cube.lengthX = cube.lengthY = cube.lengthZ = 20;
  cube.lengthX = 40;
  
  // can also be skipped since [0,0,0] is the default center
  // cube.center = [0, 0, 0];
  
  // [1,1,1] (== white) is also the default so this can be skipped aswell
  cube.color = [1, 1, 1];
  
  render.add(cube); // add the cube to the renderer


  // Add the skull
  var skull = new X.mesh()
  skull.file = "mrml/data/vtkMRMLModelNode13.stl"
  skull.opacity = 0.7;
  render.add(skull)

  var wm = new X.mesh()
  wm.file = "mrml/data/vtkMRMLModelNode4.stl"
  render.add(wm)

  render.onShowtime = function() {
    // Add a GUI
    var gui, meshGUI;
    gui = new dat.GUI({ autoPlace: false });
    var cubeGUI = gui.addFolder ( "Cube")
    cubeGUI.add(cube, 'visible')
    var lengthGUI = cubeGUI.add( cube, 'lengthX', 1, 100 ).listen()
    cubeGUI.open()
    // $("#drop2").append(gui.domElement)
    var container = document.getElementById('drop_cube')
    container.appendChild(gui.domElement)

    gui = new dat.GUI({autoPlace: false});
    meshGUI = gui.addFolder ( "Mesh" )
    meshGUI.add( skull, 'visible').listen()
    meshGUI.add( skull, 'opacity', 0, 1.0 )
    meshGUI.open()
    document.getElementById('drop_sb').appendChild ( gui.domElement )

    gui = new dat.GUI({autoPlace: false});
    meshGUI = gui.addFolder ( "Mesh" )
    meshGUI.add( wm, 'visible').listen()
    meshGUI.add( wm, 'opacity', 0, 1.0 )
    meshGUI.open()
    document.getElementById('drop_wm').appendChild ( gui.domElement )

    gui = new dat.GUI({autoPlace: false});
    meshGUI = gui.addFolder("mesh")
    meshGUI.add(wm, 'visible').listen()
    meshGUI.open()
    document.getElementById("test_div").appendChild(gui.domElement)

  }

  render.render();

cube.lengthX = 100;
})
