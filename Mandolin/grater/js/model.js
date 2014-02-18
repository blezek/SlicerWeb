
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
      for(var i = 0; i < response.mesh.length; i++) {
        this.push(new MeshModel(response.mesh[i]))
      }
      return this.models;
    }
  });

  return {
    MeshModel: MeshModel,
    MeshCollection: MeshCollection
  }
})
