from .models import Appointment
from .serializers import AppointmentSerializer
from services.appointment_service import AppointmentService
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from notifications.utils import send_appointment_email
from notifications.sms import send_sms
from notifications.service import NotificationService

class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'patient':
            raise PermissionDenied("Only patients can book appointments")
        appointment = AppointmentService.create_appointment(
            patient=user.patient,
            doctor=serializer.validated_data['doctor'],
            date=serializer.validated_data['date'],
            time=serializer.validated_data['time']
        )
        NotificationService.send_email(
            user=user,
            subject="Appointment Confirmed",
            message=f"Your appointment is booked on {appointment.date} at {appointment.time}"
        )
        NotificationService.send_sms(
            user=user,
            message=f"Appointment booked on {appointment.date} at {appointment.time}"
        )



class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user.doctor)
        elif user.role == 'patient':
            return Appointment.objects.filter(patient=user.patient)
        return Appointment.objects.all()



class AppointmentUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        if user.role != 'doctor':
            raise PermissionDenied("Only doctors can update appointments")
        serializer.save()