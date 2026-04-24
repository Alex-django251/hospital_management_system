from django.urls import path
from .views import AppointmentCreateView, AppointmentListView, AppointmentUpdateView

urlpatterns = [
    path('create/', AppointmentCreateView.as_view()),
    path('list/', AppointmentListView.as_view()),
    path('update/<int:pk>/', AppointmentUpdateView.as_view()),
]


