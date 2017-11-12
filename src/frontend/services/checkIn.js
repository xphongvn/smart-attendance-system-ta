angular.module('SmartAttendanceSystem')
.factory('CheckIn', function() {
	return {
		all: function() {
			return [
			{
				id: 1,
				dateTime: 1112222,
				status: 'in',
				studentId: 1
			},
			{
				id: 2,
				dateTime: 22112312,
				status: 'out',
				studentId: 3
			},
			{
				id: 3,
				dateTime: 21323124,
				status: 'in',
				studentId: 3
			}
			];
		},
		find: function(id) {
			return this.all().filter(function(checkIn) {
				return checkIn.studentId === id;
			});
		}
	}
})