'use strict';

/**
 * @ngdoc overview
 * @name clientApp
 * @description
 * # clientApp
 *
 * Main module of the application.
 */
angular
  .module('clientApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'angular-flot'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/sensors', {
        templateUrl: 'views/sensors.html',
        controller: 'SensorsCtrl',
        controllerAs: 'sensors'
      })
      .when('/devices', {
        templateUrl: 'views/devices.html',
        controller: 'DevicesCtrl',
        controllerAs: 'devices'
      })
      .when('/automation', {
        templateUrl: 'views/automation.html',
        controller: 'AutomationCtrl',
        controllerAs: 'automation'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
