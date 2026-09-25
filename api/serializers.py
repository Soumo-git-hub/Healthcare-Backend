from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Doctor, Patient, PatientDoctorMapping


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        read_only_fields = ['id']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        name = validated_data.pop('name')
        email = validated_data['email']
        return User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password'],
            first_name=name,
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['email'].lower(), password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'age', 'gender', 'phone', 'address',
            'medical_history', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'phone', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'doctor_specialization', 'created_at',
        ]
        read_only_fields = ['id', 'patient_name', 'doctor_name', 'doctor_specialization', 'created_at']

    def validate_patient(self, patient):
        if patient.user != self.context['request'].user:
            raise serializers.ValidationError('Invalid patient.')
        return patient

    def validate(self, attrs):
        if PatientDoctorMapping.objects.filter(
            patient=attrs['patient'],
            doctor=attrs['doctor'],
        ).exists():
            raise serializers.ValidationError('This doctor is already assigned to this patient.')
        return attrs
