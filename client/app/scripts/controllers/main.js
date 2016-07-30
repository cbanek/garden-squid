'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the clientApp
 */
angular.module('clientApp')
  .controller('MainCtrl', function ($scope, $http) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

  $scope.dataset = [];
  $scope.options = {
    legend: {
      container: '#legend',
      show: true
    }
  };

  $http.get('/api/data').then(function(response) {
    for(var key in response.data) {
      $scope.dataset.push({
        data: response.data[key],
        xaxis: {mode: 'time', timeformat: '%y/%m/%d'},
        yaxis: 1,
        label: key
      });
    }
  });

  });
