angular.module('SmartAttendanceSystem')
.factory('Student', function($resource) {
	var Student = $resource('http://localhost:8000/students');

	return Student;
})