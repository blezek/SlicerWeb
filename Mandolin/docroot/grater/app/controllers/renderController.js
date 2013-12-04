// This is the Node controller

App.RenderController = Ember.Component.extend({
	
	actions: {
		load: function ( node ) {
			alert ( "Render Controller Loading in node route" )
		},
		hide: function ( node ) {
			alert ( "Hiding in node route" )
		}, 
		report: function() { 
			alert ( 'RenderController')
		}
	}

})


App.RenderView = Ember.View.extend({
	templateName: 'render',
	didInsertElement: function () {
		console.log("Initializing Renderer")
		console.log ( "render element: ", $("#render"))
		console.log ("Controller: ", this.get('controller'))
		this.set ( 'controller.renderer', initializeRender("render") )
	}
})
