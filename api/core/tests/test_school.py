from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import School, Administrator, Teacher, Course, Student


class SchoolTests(APITestCase):
    def setUp(self):
        """
        Create a school, administrator, teacher, course and student objects to use them for the tests
        """
        self.school = School.objects.create(name='Primary School', address='Test Address')
        School.objects.create(name='Middle School', address='Test Address 1')

        self.administrator = Administrator.objects.create(name='Admin', school=self.school)
        Administrator.objects.create(name='Second Admin', school=self.school)

        self.teacher1 = Teacher.objects.create(name='Teacher 1', school=self.school)
        self.teacher2 = Teacher.objects.create(name='Teacher 2', school=self.school)

        self.course1 = Course.objects.create(
            name='Course 1', location='Room 1',
            school=self.school, teacher=self.teacher1
        )
        self.course2 = Course.objects.create(
            name='Course 2', location='Room 2',
            school=self.school, teacher=self.teacher2
        )

        self.student1 = Student.objects.create(
            name='Student 1',
            school=self.school,
            course=self.course1
        )
        self.student2 = Student.objects.create(
            name='Student 2',
            school=self.school,
            course=self.course2
        )

    def test_create_school(self):
        """
        Ensure we can create a new school
        """
        url = reverse('school-list')
        data = {'name': 'Test School', 'address': 'Test Address'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test School')

        data = {'name': '', 'address': 'Test Address'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_schools(self):
        """
        Ensure we can get all schools
        """
        url = reverse('school-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Primary School')
        self.assertEqual(response.data['results'][1]['name'], 'Middle School')

    def test_get_school(self):
        """
        Ensure we can get a school's detail
        """
        url = reverse('school-detail', kwargs={'pk': self.school.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.school.name)
        self.assertEqual(response.data['address'], self.school.address)

        url = reverse('school-detail', kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_school(self):
        """
        Ensure we can update a school's detail
        """
        url = reverse('school-detail', kwargs={'pk': self.school.id})
        data = {'name': 'First School', 'address': 'Address 1'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'First School')
        self.assertEqual(response.data['address'], 'Address 1')

        data = {'name': '', 'address': 'Address 1'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_school(self):
        """
        Ensure we can delete a school
        """
        url = reverse('school-detail', kwargs={'pk': self.school.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('school-detail', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_school_stats(self):
        """
        Ensure we can get a school's stats
        """
        url = reverse('school-stats', kwargs={'pk': self.school.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.school.id)
        self.assertEqual(response.data['courses'], 2)
        self.assertEqual(response.data['admins'], 2)
        self.assertEqual(response.data['teachers'], 2)
        self.assertEqual(response.data['students'], 2)

        url = reverse('school-stats', kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
