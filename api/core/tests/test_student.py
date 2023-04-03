from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import School, Teacher, Course, Student


class StudentTests(APITestCase):
    def setUp(self):
        """
        Create school, course and student objects to use them for the tests
        """
        self.school = School.objects.create(name='Primary School', address='Test Address')

        teacher1 = Teacher.objects.create(name='Teacher 1', school=self.school)
        teacher2 = Teacher.objects.create(name='Teacher 2', school=self.school)

        self.course1 = Course.objects.create(
            name='Course 1', location='Room 1',
            school=self.school, teacher=teacher1
        )
        self.course2 = Course.objects.create(
            name='Course 2', location='Room 2',
            school=self.school, teacher=teacher2
        )
        self.student = Student.objects.create(
            name='Student 1',
            school=self.school,
            course=self.course1
        )
        Student.objects.create(
            name='Student 2',
            school=self.school,
            course=self.course2
        )

    def test_create_student(self):
        """
        Ensure we can create a new student
        """
        url = reverse('student-list')
        data = {
            'name': 'Test Student',
            'school_id': self.school.id,
            'course_id': self.course1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Student')

        data = {'name': '', 'school_id': self.school.id, 'course_id': self.course1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_students(self):
        """
        Ensure we can get all students
        """
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Student 1')
        self.assertEqual(response.data['results'][1]['name'], 'Student 2')

    def test_get_student(self):
        """
        Ensure we can get a student's detail
        """
        url = reverse('student-detail', kwargs={'pk': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.student.name)
        self.assertEqual(response.data['school_id'], self.school.id)
        self.assertEqual(response.data['course_id'], self.course1.id)

        url = reverse('student-detail', kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_student(self):
        """
        Ensure we can update a student's detail
        """
        url = reverse('student-detail', kwargs={'pk': self.student.id})
        data = {
            'name': 'First Student',
            'school_id': self.school.id,
            'course_id': self.course2.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'First Student')
        self.assertEqual(response.data['school_id'], self.school.id)
        self.assertEqual(response.data['course_id'], self.course2.id)

        data = {'name': '', 'school_id': self.school.id, 'course_id': self.course2.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_student(self):
        """
        Ensure we can delete a student
        """
        url = reverse('student-detail', kwargs={'pk': self.student.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('student-detail', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_transfer_student(self):
        """
        Ensure we can transfer a student from one course to another
        """
        url = reverse('transfer')
        data = {
            'studentId': self.student.id,
            'fromCourseId': self.course1.id,
            'toCourseId': self.course2.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

        data = {
            'studentId': 0,
            'fromCourseId': self.course1.id,
            'toCourseId': self.course2.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['message'], 'Student doest not exist.')

        data = {
            'studentId': self.student.id,
            'fromCourseId': self.course1.id,
            'toCourseId': self.course2.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['message'], f"Student isn't included the course {self.course1.id}")

        data = {
            'studentId': self.student.id,
            'fromCourseId': self.course2.id,
            'toCourseId': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['message'], 'Course 0 does not exist')
