angular.module('SmartAttendanceSystem')
.controller('StudentCtrl', StudentCtrl);

function StudentCtrl(Student, CheckIn, $stateParams) {
	var id = parseInt($stateParams.id);

	this.user = Student.find(id);
	
	this.checkIns = CheckIn.find(id);
}