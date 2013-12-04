App.ViewRoute = Ember.Route.extend({
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
