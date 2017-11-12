angular.module('SmartAttendanceSystem')
.config(function($stateProvider) {// dependency injection
	var homeState = {
		name: 'name',
		url: '/',
		templateUrl: 'templates/home.html',
		controller: 'StudentListCtrl as vm'
	};

	var studentState = {
		name: 'student',
		url: '/student/:id',
		templateUrl: 'templates/student.html',
		controller: 'StudentCtrl as vm'
	};

	$stateProvider.state(homeState);
	$stateProvider.state(studentState);
});