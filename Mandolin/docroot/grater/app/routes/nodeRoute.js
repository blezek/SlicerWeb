App.NodeRoute = Ember.Route.extend({
	model: function() {
		console.log ( "Grabbing data!")
		var nodes = this.store.find ( 'node' )
		console.log ( nodes )
		return nodes
	},
	actions: {
		load: function ( node ) {
			alert ( "Loading in node route" )
		},
		hide: function ( node ) {
			alert ( "Hiding in node route" )
		}, 
		report: function() { 
			alert ( 'NodeRouter')
		}
	}
})

App.NodeView = Ember.View.extend({
	didInsertElement: function () {
		console.log("Initializing Renderer")
		console.log ( "render element: ", $("#render"))
		console.log ("Controller: ", this.get('controller'))
		this.set ( 'controller.renderer', initializeRender("render") )
	}
})
