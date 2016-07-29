'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the clientApp
 */
angular.module('clientApp')
  .controller('MainCtrl', function ($scope) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

  $scope.dataset = [{ data: [], yaxis: 1, label: 'sin' }];
  $scope.options = {
    legend: {
      container: '#legend',
      show: true
    }
  };

  for (var i = 0; i < 14; i += 0.5) {
    $scope.dataset[0].data.push([i, Math.sin(i)]);
  }

  });
