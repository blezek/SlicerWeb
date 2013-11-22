App = Ember.Application.create()


// Routes go here
App.Router.map(function() {
	this.route("node")
})

// Connecting to Slicer
App.ApplicationAdapter = DS.RESTAdapter.extend({
  namespace: '../..'
});