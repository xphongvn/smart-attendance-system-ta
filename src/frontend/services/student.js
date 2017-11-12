angular.module('SmartAttendanceSystem')
.factory('Student', function() {
	return {
		all: function() {
			return [
			{
				id: 1,
				name: 'Alec Blagg',
				picture: 'http://localhost:3000/Alec_0.jpg',
				status: 'in'
			},
			{
				id: 2,
				name: 'Emil Balian',
				picture: 'http://localhost:3000/Emil_4.jpg',
				status: 'in'
			},
			{
				id: 3,
				name: 'Greg Crow',
				picture: 'http://localhost:3000/Greg_3.jpg',
				status: 'out'
			}
			];
		},
		find: function(id) {
			return this.all().find(function(student) {
				return student.id === id;
			});
		}
	}
})