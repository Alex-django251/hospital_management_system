from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('post-login-redirect/', views.post_login_redirect),
    path('doctor/dashboard/', views.doctor_dashboard),
    path('patient/dashboard/', views.patient_dashboard),
    path('receptionist/dashboard/', views.receptionist_dashboard),
]


