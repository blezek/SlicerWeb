

/////////  Display No more



  // include all used X-classes here
  // this is only required when using the xtk-deps.js file
  goog.require('X.renderer3D');
  goog.require('X.cube');
  goog.require('X.mesh');


function initializeRender(container) {
// create and initialize a 3D renderer
  var r = new X.renderer3D();
  r.container = container
  r.init();
  // create a cube
  cube = new X.cube();
  
  // setting the edge length can also be skipped since 20 is the default
  cube.lengthX = cube.lengthY = cube.lengthZ = 20;
  
  // can also be skipped since [0,0,0] is the default center
  cube.center = [0, 0, 0];
  
  // [1,1,1] (== white) is also the default so this can be skipped aswell
  cube.color = [0, 0, 1];
  
  r.add(cube); // add the cube to the renderer
  r.render();
  return r;
  }


App.DisplayView = Ember.View.extend({
	templateName: 'display',
	didInsertElement: function () {
		console.log("Initializing Renderer")
		
		console.log ( "render element: ", $("#render"))
		console.log ("Controller: ", this.get('controller'))
		this.set ( 'controller.renderer', initializeRender("render") )
	}
})

App.DisplayController = Ember.Controller.extend({
	needs: 'node',
	display: 'something',
	actions: {
		toggle: function(node) {
			// Check to see if we have a renderable object attached
			if ( !node.get('displayNode')) {
				var renderer = this.get("renderer")
				var mesh = new X.mesh()
				mesh.file = "../../../mrml/data/" + node.id + ".stl"
				console.log("Rendering", node)
				console.log('Color of the node is: ' + node.get('data').color)
				var color = node.get('data').color
				var a = color.split ( ',').map(Number)

				console.log ( "Color:", color, a)
			    // mesh.file = 'http://x.babymri.org/?porsche.stl';
			    mesh.color = a

			    console.log("Loading: " + mesh.file)
			    node.set('displayNode', mesh )
			    renderer.add(node.get('displayNode'))
			}
			node.get('displayNode').visible = node.get('display');
		}
	}
})

