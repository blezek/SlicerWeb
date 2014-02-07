

  render = new X.renderer3D();
  render.container = "render"
  render.init();

  // create a cube
  cube = new X.cube();
  
  // setting the edge length can also be skipped since 20 is the default
  cube.lengthX = cube.lengthY = cube.lengthZ = 20;
  
  // can also be skipped since [0,0,0] is the default center
  // cube.center = [0, 0, 0];
  
  // [1,1,1] (== white) is also the default so this can be skipped aswell
  cube.color = [0, 0, 1];
  
  render.add(cube); // add the cube to the renderer
  render.render();