
require.config({
  deps: ['./foundation', './xtk', 'dat.gui'],
  shim: {
    'foundation': {
      deps: ['jquery'],
      exports: 'foundation'
    },
    'angular': {
      exports: 'angular'
    },
    'angularAMD':['angular'],
    'ngload':['angularAMD']
  }
})

// Fire up foundation
require(['jquery', 'foundation'], function(jquery, foundation) {
 jquery(document).foundation();

})




require(["model", 'angular', 'angularAMD'], function(model, angular, angularAMD) {
// include all used X-classes here
  // this is only required when using the xtk-deps.js file
/*
  goog.require('X.renderer3D');
  goog.require('X.cube');
  goog.require('X.mesh');
*/


  render = new X.renderer3D();
  render.container = "render"
  render.init();

  meshCollection = new model.MeshCollection();
  // setInterval ( function() { meshCollection.fetch({remove: true}) }, 2000 );


  console.log ( "Creating graterApp")
  // create the angular application
  var graterApp = angular.module ( 'graterApp', [] );

  // This is a custom directive to create our GUI as needed
  graterApp.directive("meshControls", function() {
    return function(scope, element, attrs) {
      console.log ( "processing", scope, element, attrs);
      var m = new X.mesh()
      m.file = "mrml/data/" + scope.mesh.id + ".stl"
      render.add ( m )

      var gui, meshGUI;
      gui = new dat.GUI({ autoPlace: false });
      meshGUI = gui.addFolder ( scope.mesh.attributes.Name )
      meshGUI.add( m, 'visible').listen()
      meshGUI.add( m, 'opacity', 0, 1.0 )
      // meshGUI.open()
      element.append( gui.domElement )
    }
  })

  graterApp.controller ( 'MeshListController', function($scope, $timeout ) {
    meshCollection.fetch({remove: true})
    $scope.meshCollection = meshCollection;
    $scope.render = render;
    (function tock() {
      meshCollection.fetch({remove:true});
      console.log("tock!")
      // $scope.meshCollection = meshCollection;
      $timeout(tock,2000);
    })();
  })
  angularAMD.bootstrap(graterApp)

  

  render.render();

})
