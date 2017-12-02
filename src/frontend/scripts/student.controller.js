angular.module('SmartAttendanceSystem')
.controller('StudentCtrl', StudentCtrl);

function StudentCtrl(Student, CheckIn, $stateParams) {
	this.user = Student.get({ id: $stateParams.id });

  this.user.$promise.then(user => {
    this.checkIns = CheckIn.query({
      classifyId: user.classifyId
    });
  });
}