'use strict';


// Declare app level module which depends on filters, and services
angular.module('grater', [
  'ngRoute',
  'grater.filters',
  'grater.services',
  'grater.directives',
  'grater.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {templateUrl: 'partials/menu.html', controller: 'MenuCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});
}]);
