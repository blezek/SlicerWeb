

// Configuration for require.js
// foundation, xtk and dat.gui are loaded by default
require.config({
  deps: ['./foundation', './xtk', 'dat.gui'],

  // Some packages do not provide require info, so we 'shim' them here
  shim: {
    'foundation': {
      deps: ['jquery', 'modernizr'],
      exports: 'foundation'
    },
    'angular': {
      exports: 'angular'
    },
    // The angularAMD and ngload let us load a page and add angular apps later
    'angularAMD':['angular'],
    'ngload':['angularAMD']
  }
})

// Fire up foundation on document load
require(['jquery', 'foundation'], function(jquery, foundation) {
 jquery(document).foundation();

})


// For Grater to work, the model, angular and angularAMD packages are required
require(["model", 'angular', 'angularAMD', 'grater.io'], function(model, angular, angularAMD, io) {
  // Intentionally expose render and meshCollection as global variables
  render = new X.renderer3D();
  render.container = "render"
  render.init();

  socket = io.connect("ws://" + location.hostname + ":9999")
  socket.on("hello", function(data) {
    console.log(data);
  })
  socket.on("camera", function(data) {
    // camera = $scope.activeCamera
    render.camera.position = data.position
    render.camera.up = data.view_up
    render.camera.focus = data.focal_point
  })

  meshCollection = new model.MeshCollection();

  console.log ( "Creating graterApp")

  // create the angular application
  var graterApp = angular.module ( 'graterApp', [] );

  // A mesh's attributes from the Backbone model
  var setAttributes = function( m, mesh ) {
    m.visible = mesh.get("display_visibility")
    m.opacity = mesh.get("opacity")
    m.color = mesh.get('color')
  }


  // This is a custom directive to create our GUI as needed
  graterApp.directive("meshControls", function() {
    return function(scope, element, attrs) {

      var m = new X.mesh()
      m.file = "mrml/data/" + scope.mesh.id + ".stl"
      m.color = scope.mesh.get('color')
      render.add ( m )

      var gui, meshGUI;
      gui = new dat.GUI({ autoPlace: false });
      meshGUI = gui.addFolder ( scope.mesh.get('Name') )
      meshGUI.add( m, 'visible').listen()
      meshGUI.add( m, 'opacity', 0, 1.0 ).listen()
      element.append( gui.domElement )

      // Set the initial values
      setAttributes ( m, scope.mesh );

      // Sync the Backbone model to the XTK mesh object
      scope.mesh.on("change", function() {
        setAttributes ( m, this )
      })

      scope.mesh.on("request", function() {
        console.log ( "Beggining Request")
      })

      // Remove the mesh object from the renderer when it goes away in the collection
      scope.mesh.on ( 'remove', function() {
        m.visible = false
        render.remove ( m )
      })

    }
  })

  graterApp.controller ( 'MeshListController', function($scope, $timeout ) {

    // Grab the initial set of mesh objects.  When the collection changes,
    // Angular automagically adds the new objects into our list.
    // The meshControls directive handles updates and item deletion.
    meshCollection.fetch({remove: true})
    $scope.meshCollection = meshCollection;
    $scope.render = render;
    // Fetch the collection every 2 seconds
    (function tock() {
      meshCollection.fetch({remove:true});
      $timeout(tock,20000);
    })();
  });


  // An angular controller for the camera
  graterApp.controller ( 'CameraController', function($scope, $timeout ) {
    $scope.cameraCollection = new model.CameraCollection;
    // Fetch the camera list from Slicer and set the active to the first one.
    $scope.activeCamera = null
    $scope.cameraCollection.fetch({remove: true,
      success: function() {
        $scope.activeCamera = $scope.cameraCollection.models[0]        
      }
    })
    $scope.render = render;
    $scope.setCamera = function(camera) {
      $scope.activeCamera = camera.id
    };

    // Every 500ms, update the cameras
    (function cameratock() {
      $scope.cameraCollection.fetch({remove:true});
      $timeout(cameratock,5000);
    })();
  })

  // Here is where the fun happens.  angularAMD contains support for initializing an angular
  // app after the page load.
  angularAMD.bootstrap(graterApp)

  // Tell XTK to start rendering.
  render.render();

})
