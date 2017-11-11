angular.module('SmartAttendanceSystem')
.config(function($stateProvider) {// dependency injection
	var homeState = {
		name: 'name',
		url: '/',
		templateUrl: 'templates/home.html',
		controller: 'StudentListCtrl as vm'
	};

	$stateProvider.state(homeState);
});