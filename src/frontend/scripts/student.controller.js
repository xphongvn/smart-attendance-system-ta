angular.module('SmartAttendanceSystem')
.controller('StudentCtrl', StudentCtrl);

function StudentCtrl(Student, CheckIn, $stateParams) {
	this.user = Student.get({ id: $stateParams.id });

	//this.checkIns = CheckIn.find(id);
}