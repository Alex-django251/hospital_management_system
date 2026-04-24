from django.urls import path
from .views import (
    ReceptionistDashboardView,
    CreatePatientView,
    CreateAppointmentByReceptionist,
    AllAppointmentsView,
    PatientListView
)

urlpatterns = [
    path('dashboard/', ReceptionistDashboardView.as_view()),
    path('create-patient/', CreatePatientView.as_view()),
    path('patients/', PatientListView.as_view()),
    path('create-appointment/', CreateAppointmentByReceptionist.as_view()),
    path('appointments/', AllAppointmentsView.as_view()),
]

