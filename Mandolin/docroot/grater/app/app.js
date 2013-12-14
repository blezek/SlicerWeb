// App = Ember.Application.create({})


// // Routes go here
// App.Router.map(function() {
// 	// this.resource("about")
// 	this.resource("view")
// // 	this.resource("render")
// })


App = Ember.Application.create({})

// Connecting to Slicer
App.ApplicationAdapter = DS.RESTAdapter.extend({
  namespace: '../..'
});




// Routes go here
App.Router.map(function() {
	this.resource("viewer")
})


App.ViewerRoute = Ember.Route.extend({
  setupController: function(controller, model) {
  	var nodes = this.store.find ( 'node' )
  	console.log ( nodes )

    this.controllerFor('node').set('model', nodes);
    this.controllerFor('display').set('model', nodes);
  }
});

