angular.module('SmartAttendanceSystem')
.controller('StudentListCtrl', StudentListCtrl);

function StudentListCtrl(Student, $http) {
  $http.get('http://localhost:8000/students/').then(response => {
    this.students = response.data;
  });
}