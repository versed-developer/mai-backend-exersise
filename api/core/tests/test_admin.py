from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import School, Administrator


class AdministratorTests(APITestCase):
    def setUp(self):
        """
        Create a school object and administrator objects to use them for the tests
        """
        self.school = School.objects.create(name='Primary School', address='Test Address')

        self.administrator = Administrator.objects.create(name='Admin', school=self.school)
        Administrator.objects.create(name='Second Admin', school=self.school)

    def test_create_administrator(self):
        """
        Ensure we can create a new administrator
        """
        url = reverse('administrator-list')
        data = {'name': 'Test Admin', 'school_id': self.school.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Admin')

        data = {'name': '', 'school_id': self.school.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_administrators(self):
        """
        Ensure we can get all administrators
        """
        url = reverse('administrator-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Admin')
        self.assertEqual(response.data['results'][1]['name'], 'Second Admin')

    def test_get_administrator(self):
        """
        Ensure we can get an administrator's detail
        """
        url = reverse('administrator-detail', kwargs={'pk': self.administrator.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.administrator.name)
        self.assertEqual(response.data['school_id'], self.school.id)

        url = reverse('administrator-detail', kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_administrator(self):
        """
        Ensure we can update an administrator's detail
        """
        url = reverse('administrator-detail', kwargs={'pk': self.administrator.id})
        data = {'name': 'First Admin', 'school_id': self.school.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'First Admin')
        self.assertEqual(response.data['school_id'], self.school.id)

        data = {'name': '', 'school_id': self.school.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_administrator(self):
        """
        Ensure we can delete an administrator
        """
        url = reverse('administrator-detail', kwargs={'pk': self.administrator.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('administrator-detail', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
