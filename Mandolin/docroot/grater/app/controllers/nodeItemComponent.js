App.NodeItemComponent = Ember.Component.extend({
	actions: {
		load: function(node){
			alert ( "Loading: " + node + " name: " + node.get ( 'name'))
		},
		toggleBody: function() {
			console.log ("Toggle Body")
			this.toggleProperty('isShowingBody')
		},
		report: function() {
			alert ( "Alert from NodeItem Component")
		}
	}
})