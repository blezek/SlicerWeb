'use strict';

/* Controllers */

angular.module('grater.controllers', []).
  controller('MenuCtrl', ['$scope', '$http', function($scope, $http) {
  	$http.get('/mrml/models').success ( function (data) {
  		$scope.models = data.nodes
  	})
  }]);