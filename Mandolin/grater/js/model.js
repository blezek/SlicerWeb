
define(function(require) {
  "use strict";
  var $ = require('jquery'),
  Backbone = require('backbone');

  var MeshModel = Backbone.Model.extend({
    urlRoot: '/rest/mesh'
  });

  var MeshCollection = Backbone.Collection.extend({
    model: MeshModel,
    url: '/rest/mesh',
    parse: function(response) {
      var m = [];
      for(var i = 0; i < response.mesh.length; i++) {
        m.push(new MeshModel(response.mesh[i]))
      }
      this.set ( m )
      return this.models;
    }
  });


  var CameraModel = Backbone.Model.extend({
    urlRoot: '/rest/cameras'
  });

  var CameraCollection = Backbone.Collection.extend({
    model: CameraModel,
    url: '/rest/cameras',
    parse: function(response) {
      var m = [];
      for(var i = 0; i < response.cameras.length; i++) {
        m.push(new CameraModel(response.cameras[i]))
      }
      this.set ( m )
      return this.models;
    }
  })


  return {
    MeshModel: MeshModel,
    MeshCollection: MeshCollection,
    CameraModel: CameraModel,
    CameraCollection: CameraCollection
  }
})
