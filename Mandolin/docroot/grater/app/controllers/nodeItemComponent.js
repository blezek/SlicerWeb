App.NodeItemComponent = Ember.Component.extend({
	actions: {
		toggleBody: function() {
			console.log ("Toggle Body")
			this.toggleProperty('isShowingBody')
		}
	}
})