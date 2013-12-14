// // This is the Node controller


// App.NodeView = Ember.View.extend({
// 	templateName: 'node'
// })

// App.NodeController = Ember.Component.extend({
// 	needs: 'display',
// 	actions: {
// 		display: function ( node ) {
// 			console.log(this.get('controllers'))
// 			var n = this.get('controllers.display')
// 			console.log ( n )
// 			n.send ( 'display', node)

// 			alert ( "Loading in node route" )
// 		},
// 		hide: function ( node ) {
// 			alert ( "Hiding in node route" )
// 		}, 
// 		report: function() { 
// 			var rc = this.get('controllers')
// 			console.log ( rc )
// 			alert ( 'NodeController, now sending to ' + rc)
// 		},
// 		toggleBody: function(node) {
// 			node.toggleProperty ( 'isShowingBody' )
// 		}
// 	}

// })




/////////  Node

App.NodeView = Ember.View.extend({
	templateName: 'node',
	name: 'NodeView'
})


App.NodeController = Ember.Controller.extend({
	needs: 'display',
	
	actions: {
		hi: function(greeting) {
			alert ( "Hi from NodeController.  My model is: " + this.get('model') + " " + greeting)
		},
		toggle: function(node) {
			var n = this.get('controllers.display')
			node.toggleProperty("display")
			n.send ( 'toggle', node)
			this.set ( 'selected', node)
		},
		display: function ( node ) {
			console.log(this.get('controllers'))
			var n = this.get('controllers.display')
			console.log ( n )
			n.send ( 'display', node)

			console.log ( "Loading in node route" )
		},
		hide: function ( node ) {
			alert ( "Hiding in node route" )
		}, 
		report: function() { 
			var rc = this.get('controllers')
			console.log ( rc )
			alert ( 'NodeController, now sending to ' + rc)
		},
		toggleBody: function(node) {
			node.toggleProperty ( 'isShowingBody' )
		}
	}
})
