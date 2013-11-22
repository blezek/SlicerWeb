App.NodeRoute = Ember.Route.extend({
	model: function() {
		console.log ( "Grabbing data!")
		var nodes = this.store.find ( 'node' )
		console.log ( nodes )
		return nodes
	}
})