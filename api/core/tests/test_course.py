from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import School, Teacher, Course


class CourseTests(APITestCase):
    def setUp(self):
        """
        Create school, teacher and course objects to use them for the tests
        """
        self.school = School.objects.create(name='Primary School', address='Test Address')

        self.teacher1 = Teacher.objects.create(name='Teacher 1', school=self.school)
        self.teacher2 = Teacher.objects.create(name='Teacher 2', school=self.school)

        self.course = Course.objects.create(
            name='Course 1', location='Room 1',
            school=self.school, teacher=self.teacher1
        )
        Course.objects.create(
            name='Course 2', location='Room 2',
            school=self.school, teacher=self.teacher2
        )

    def test_create_course(self):
        """
        Ensure we can create a new course
        """
        url = reverse('course-list')
        data = {
            'name': 'Test Course',
            'location': 'Test Room',
            'school_id': self.school.id,
            'teacher_id': self.teacher1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Course')

        data = {'name': '', 'location': 'Test Room', 'school_id': self.school.id, 'teacher_id': self.teacher1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_courses(self):
        """
        Ensure we can get all courses
        """
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Course 1')
        self.assertEqual(response.data['results'][1]['name'], 'Course 2')

    def test_get_course(self):
        """
        Ensure we can get a course's detail
        """
        url = reverse('course-detail', kwargs={'pk': self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.course.name)
        self.assertEqual(response.data['location'], self.course.location)
        self.assertEqual(response.data['school_id'], self.school.id)
        self.assertEqual(response.data['teacher_id'], self.teacher1.id)

        url = reverse('course-detail', kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_course(self):
        """
        Ensure we can update a course's detail
        """
        url = reverse('course-detail', kwargs={'pk': self.course.id})
        data = {
            'name': 'First Course',
            'location': 'First Room',
            'school_id': self.school.id,
            'teacher_id': self.teacher2.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'First Course')
        self.assertEqual(response.data['location'], 'First Room')
        self.assertEqual(response.data['school_id'], self.school.id)
        self.assertEqual(response.data['teacher_id'], self.teacher2.id)

        data = {'name': '', 'location': 'First Room', 'school_id': self.school.id, 'teacher_id': self.teacher2.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_course(self):
        """
        Ensure we can delete a course
        """
        url = reverse('course-detail', kwargs={'pk': self.course.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('course-detail', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
