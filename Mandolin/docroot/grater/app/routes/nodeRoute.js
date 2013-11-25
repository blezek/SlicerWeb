App.NodeRoute = Ember.Route.extend({
	model: function() {
		console.log ( "Grabbing data!")
		var nodes = this.store.find ( 'node' )
		console.log ( nodes )
		return nodes
	}
})

App.NodeView = Ember.View.extend({
	didInsertElement: function () {
		console.log("Initializing Renderer")
		console.log ( "render element: ", $("#render"))
		initializeRender("render")
	}
})
