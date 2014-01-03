

/////////  Display No more

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

// // This is the Node controller



// // App.RenderView = Ember.View.extend({
// // 	templateName: 'render'
// // 	// ,
// // // 	didInsertElement: function () {
// // // 		console.log("Initializing Renderer")
// // // 		console.log ( "render element: ", $("#render"))
// // // 		console.log ("Controller: ", this.get('controller'))
// // // 		this.set ( 'controller.renderer', initializeRender("render") )
// // // 	}
// // })

// // App.RenderController = Ember.Component.extend({
// // 	needs: 'node',
// // 	actions: {
// // 		display: function ( node ) {
// // 			alert ( "Render Controller Loading in node route" )
// // 		},
// // 		hide: function ( node ) {
// // 			alert ( "Hiding in node route" )
// // 		}, 
// // 		report: function() { 
// // 			alert ( 'RenderController')
// // 		}
// // 	}

// // })



// /////////  Display

// App.DisplayView = Ember.View.extend({
// 	templateName: 'display'
// })

// App.DisplayController = Ember.Controller.extend({
// 	needs: 'node',
// 	display: 'something',
// 	actions: {
// 		hi: function() {
// 			var n = this.get('controllers.node')
// 			console.log ( n )
// 			alert ( "Hi from DisplayController")
// 			// Send an action to NodeController
// 			n.send('hi', ' from DisplayController')
// 		},
// 		toggle: function(node) {
// 			console.log("DisplayController: toggle " + node)
// 			console.log("Current list is: " + this.get ( 'display' ) )
// 			// this.set ( 'displayList',[node])
// 			this.set ( 'display', node)
// 		}
// 	}
// })