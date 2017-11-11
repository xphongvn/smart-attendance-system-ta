angular.module('SmartAttendanceSystem')
.controller('StudentCtrl', StudentCtrl);

function StudentCtrl() {
	this.user = {
		id: 1,
		name: 'Greg Crow',
		picture: 'http://localhost:3000/Greg_3.jpg',
		status: 'in'
	};
	
	this.checkIns = [
	{
		id: 1,
		dateTime: 1112222,
		status: 'in'
	},
	{
		id: 2,
		dateTime: 22112312,
		status: 'out'
	},
	{
		id: 3,
		dateTime: 21323124,
		status: 'in'
	}
	]
}