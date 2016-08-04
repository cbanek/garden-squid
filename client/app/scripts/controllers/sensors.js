'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:SensorsCtrl
 * @description Angular controller for dealing with sensor assignment.
 */
angular.module('clientApp')
  .controller('SensorsCtrl', function ($scope, $http) {
    $scope.reset = function() {
      $http.get('/api/sensors').then(function(response) {
        $scope.saveModel = 'reset';
        $scope.sensors = response.data;
      });
    };

    $scope.modified = function() {
      $scope.saveModel = 'modified';
    };

    $scope.save = function() {
      $http.put('/api/sensors', $scope.sensors)
        .then(function success() {
          $scope.reset();
        }, function error() {
          $scope.modified();
        });
    };

    $scope.reset();
  });
