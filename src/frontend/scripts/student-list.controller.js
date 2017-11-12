angular.module('SmartAttendanceSystem')
.controller('StudentListCtrl', StudentListCtrl);

function StudentListCtrl(Student) {
  this.students = Student.all();
}

// {
//   field: value
// }
//
//  ng-if