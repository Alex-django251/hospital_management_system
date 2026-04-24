from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from datetime import date
from appointments.models import Appointment
from prescriptions.models import Prescription


class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'doctor':
            raise PermissionDenied("Only doctors allowed")
        doctor = user.doctor
        appointments = Appointment.objects.filter(doctor=doctor)
        return Response({
            "total_appointments": appointments.count(),
            "today_appointments": appointments.filter(date=date.today()).count(),
            "pending": appointments.filter(status='pending').count(),
            "completed": appointments.filter(status='completed').count(),
        })
        
        