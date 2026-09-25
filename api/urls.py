from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DoctorViewSet,
    LoginView,
    MappingListCreateView,
    MappingPatientOrDeleteView,
    PatientViewSet,
    RegisterView,
)

router = DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('doctors', DoctorViewSet, basename='doctors')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('mappings/', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('mappings/<int:lookup_id>/', MappingPatientOrDeleteView.as_view(), name='mapping-patient-or-delete'),
    path('', include(router.urls)),
]
