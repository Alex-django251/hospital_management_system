from django.urls import path
from .views import PrescriptionCreateView,PrescriptionListView, PatientProfileView , PatientReportView, PrescriptionPDFView

urlpatterns = [
    path('create/', PrescriptionCreateView.as_view()),
    path('list/', PrescriptionListView.as_view()),
    path('patient/profile/', PatientProfileView.as_view()),
    path('patient/report/', PatientReportView.as_view()),
    path('prescription/<int:pk>/pdf/', PrescriptionPDFView.as_view()),
]

