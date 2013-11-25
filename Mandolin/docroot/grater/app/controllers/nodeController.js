// This is the Node controller

App.NodeController = Ember.Component.extend({
	renderer: null,
	
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
