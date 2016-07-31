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

  $scope.dateOptions = {
    formatYear: 'yy',
    startingDay: 1
  };

  $scope.toTime = {
    time: new Date(),
    opened: false
  };

  $scope.fromTime = {
    time: new Date(),
    opened: false
  };

  $scope.fromTime.time.setDate($scope.toTime.time.getDate() - 1);

  $scope.dataset = [];
  $scope.options = {
    xaxes: [{mode: 'time', timeformat: '%y/%m/%d'}],
    yaxes: [{min:10}, {min:300, position: 'right'}],
    legend: {
      container: '#legend',
      show: true,
      noColumns: 10
    }
  };

  $scope.draw = function() {
    var params = {
      from: $scope.fromTime.time.toISOString().split('.')[0],
      to: $scope.toTime.time.toISOString().split('.')[0]
    };

    $http.get('/api/data', {params: params}).then(function(response) {
      $scope.dataset = [];

      for(var key in response.data) {
        var axis;
        if (key === ' co2') {
          console.log('key is %s', key);
          axis = 2;
        } else {
          axis = 1;
        }

        $scope.dataset.push({
          data: response.data[key],
          yaxis: axis,
          label: key
        });
      }
    });
  };

  });
