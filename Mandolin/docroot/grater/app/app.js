App = Ember.Application.create({})


// Routes go here
App.Router.map(function() {
	this.resource("node")
	this.resource("about")
})

// Connecting to Slicer
App.ApplicationAdapter = DS.RESTAdapter.extend({
  namespace: '../..'
});