angular.module('SmartAttendanceSystem')
.controller('StudentListCtrl', StudentListCtrl);

function StudentListCtrl() {
  this.students = [
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
}

// {
//   field: value
// }
//
//  ng-if