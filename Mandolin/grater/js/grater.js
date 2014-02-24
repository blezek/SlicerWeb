
require.config({
  deps: ['./foundation', './xtk', 'dat.gui'],
  shim: {
    'foundation': {
      deps: ['jquery', 'modernizr'],
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
      m.color = scope.mesh.get('color')
      render.add ( m )

      var gui, meshGUI;
      gui = new dat.GUI({ autoPlace: false });
      meshGUI = gui.addFolder ( scope.mesh.get('Name') )
      meshGUI.add( m, 'visible').listen()
      meshGUI.add( m, 'opacity', 0, 1.0 ).listen()
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
  });


  graterApp.controller ( 'CameraController', function($scope, $timeout ) {
    $scope.cameraCollection = new model.CameraCollection;
    $scope.cameraCollection.fetch({remove: true})
    $scope.activeCamera = $scope.cameraCollection.models[0]
    $scope.render = render;
    $scope.setCamera = function(camera) {
      console.log("set active camera to: ", camera)
      $scope.activeCamera = camera
    };
    (function cameratock() {
      $scope.cameraCollection.fetch({remove:true});
      console.log($scope.activeCamera)
      if ( $scope.activeCamera ) {
        $scope.render.camera.position = $scope.activeCamera.get('Position')
      }

      $timeout(cameratock,500);
    })();
  })

  angularAMD.bootstrap(graterApp)

  

  render.render();

})
