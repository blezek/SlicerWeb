
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

  return {
    MeshModel: MeshModel,
    MeshCollection: MeshCollection
  }
})
