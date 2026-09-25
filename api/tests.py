from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Doctor, Patient, PatientDoctorMapping


class HealthcareApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def authenticate(self, email='user@example.com', password='StrongPass123'):
        user = User.objects.create_user(username=email, email=email, password=password)
        self.client.force_authenticate(user=user)
        return user

    def test_register_and_login(self):
        response = self.client.post('/api/auth/register/', {
            'name': 'Asha Sharma',
            'email': 'asha@example.com',
            'password': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/auth/login/', {
            'email': 'asha@example.com',
            'password': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_patient_list_only_returns_authenticated_users_patients(self):
        user = self.authenticate()
        other = User.objects.create_user(username='other@example.com', email='other@example.com')
        Patient.objects.create(user=other, name='Hidden Patient', age=40, gender='other')

        self.client.post('/api/patients/', {'name': 'Visible Patient', 'age': 28, 'gender': 'female'})
        response = self.client.get('/api/patients/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Visible Patient')
        self.assertEqual(Patient.objects.filter(user=user).count(), 1)

    def test_doctor_and_mapping_flow(self):
        user = self.authenticate()
        patient = Patient.objects.create(user=user, name='Patient One', age=30, gender='male')
        doctor = Doctor.objects.create(name='Dr Rao', specialization='Cardiology')

        response = self.client.post('/api/mappings/', {'patient': patient.id, 'doctor': doctor.id})
        self.assertEqual(response.status_code, 201)

        response = self.client.get(f'/api/mappings/{patient.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['doctor_name'], 'Dr Rao')

        mapping = PatientDoctorMapping.objects.get(patient=patient, doctor=doctor)
        response = self.client.delete(f'/api/mappings/{mapping.id}/')
        self.assertEqual(response.status_code, 204)
