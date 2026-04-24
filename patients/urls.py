from django.urls import path
from .views import PatientDashboardView, PatientMedicalHistoryView

urlpatterns = [
    path('dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('medical-history/', PatientMedicalHistoryView.as_view()),
]