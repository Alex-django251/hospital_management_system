from django.urls import path
from .views import (
    LabReportCreateView,
    LabReportListView,
    download_lab_report,
    LabReportView
)

urlpatterns = [
    path('create/', LabReportCreateView.as_view()),
    path('', LabReportView.as_view(), name='lab-reports'),
    path('list/', LabReportListView.as_view()),
    path('<int:pk>/download/', download_lab_report),
]