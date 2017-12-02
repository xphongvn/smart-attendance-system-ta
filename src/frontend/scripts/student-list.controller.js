angular.module('SmartAttendanceSystem')
.controller('StudentListCtrl', StudentListCtrl);

function StudentListCtrl(Student, $http) {
  this.students = Student.query();
}