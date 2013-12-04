// This is the Node controller

App.NodeController = Ember.Component.extend({
	needs: 'render',
	actions: {
		load: function ( node ) {
			alert ( "Loading in node route" )
		},
		hide: function ( node ) {
			alert ( "Hiding in node route" )
		}, 
		report: function() { 
			var rc = this.get('controllers')
			console.log ( rc )
			alert ( 'NodeController, now sending to ' + rc)
		}
	}

})


App.NodeView = Ember.View.extend({
	templateName: 'node',
	name: 'NodeView'
})
