from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import School, Teacher


class TeacherTests(APITestCase):
    def setUp(self):
        """
        Create a school object and teacher objects to use them for the tests
        """
        self.school = School.objects.create(name='Primary School', address='Test Address')

        self.teacher = Teacher.objects.create(name='Teacher 1', school=self.school)
        Teacher.objects.create(name='Teacher 2', school=self.school)

    def test_create_teacher(self):
        """
        Ensure we can create a new teacher
        """
        url = reverse('teacher-list')
        data = {'name': 'Test Teacher', 'school_id': self.school.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Teacher')

        data = {'name': '', 'school_id': self.school.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_teachers(self):
        """
        Ensure we can get all teachers
        """
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Teacher 1')
        self.assertEqual(response.data['results'][1]['name'], 'Teacher 2')

    def test_get_teacher(self):
        """
        Ensure we can get a teacher's detail
        """
        url = reverse('teacher-detail', kwargs={'pk': self.teacher.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.teacher.name)
        self.assertEqual(response.data['school_id'], self.school.id)

        url = reverse('teacher-detail', kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_teacher(self):
        """
        Ensure we can update teacher detail
        """
        url = reverse('teacher-detail', kwargs={'pk': self.teacher.id})
        data = {'name': 'First Teacher', 'school_id': self.school.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'First Teacher')
        self.assertEqual(response.data['school_id'], self.school.id)

        data = {'name': '', 'school_id': self.school.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_teacher(self):
        """
        Ensure we can delete a teacher
        """
        url = reverse('teacher-detail', kwargs={'pk': self.teacher.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('teacher-detail', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
