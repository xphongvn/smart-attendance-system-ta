angular.module('SmartAttendanceSystem')
.factory('CheckIn', function($resource) {
	var CheckIn = $resource('http://localhost:8000/checkins/:id');
	return CheckIn;
})