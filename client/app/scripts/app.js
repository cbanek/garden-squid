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
    'angular-flot',
    'ui.bootstrap'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/config', {
        templateUrl: 'views/config.html',
        controller: 'ConfigCtrl',
        controllerAs: 'config'
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
