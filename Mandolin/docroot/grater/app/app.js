App = Ember.Application.create({})


// Routes go here
App.Router.map(function() {
	this.resource("about")
	this.resource("view")
// 	this.resource("render")
})

// Connecting to Slicer
App.ApplicationAdapter = DS.RESTAdapter.extend({
  namespace: '../..'
});