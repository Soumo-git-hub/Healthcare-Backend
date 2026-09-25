from rest_framework import generics, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import (
    DoctorSerializer,
    LoginSerializer,
    PatientDoctorMappingSerializer,
    PatientSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer

    def get_queryset(self):
        return PatientDoctorMapping.objects.select_related('patient', 'doctor').filter(
            patient__user=self.request.user
        )


class MappingPatientOrDeleteView(APIView):
    def get(self, request, lookup_id):
        if not Patient.objects.filter(id=lookup_id, user=request.user).exists():
            raise NotFound('Patient not found.')

        mappings = PatientDoctorMapping.objects.select_related('patient', 'doctor').filter(
            patient_id=lookup_id
        )
        serializer = PatientDoctorMappingSerializer(mappings, many=True, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, lookup_id):
        mapping = PatientDoctorMapping.objects.filter(
            id=lookup_id,
            patient__user=request.user,
        ).first()
        if not mapping:
            raise NotFound('Mapping not found.')

        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
