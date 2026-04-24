from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from appointments.models import Appointment
from prescriptions.models import Prescription


def get_patient_data(patient):
    appointments = Appointment.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)
    return appointments, prescriptions


class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'patient':
            raise PermissionDenied("Only patients can access dashboard")
        patient = user.patient
        appointments, prescriptions = get_patient_data(patient)
        return Response({
            "message": "Patient Dashboard",
            "stats": {
                "total_appointments": appointments.count(),
                "pending": appointments.filter(status='pending').count(),
                "completed": appointments.filter(status='completed').count(),
            },
            "recent_appointments": [
                {
                    "id": a.id,
                    "doctor": a.doctor.user.username,
                    "date": a.date,
                    "status": a.status
                }
                for a in appointments[:5]
            ],

            "recent_prescriptions": [
                {
                    "id": p.id,
                    "doctor": p.doctor.user.username,
                    "medicines": p.medicines,
                    "date": p.created_at
                }
                for p in prescriptions[:5]
            ]
        })


class PatientMedicalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'patient':
            raise PermissionDenied("Only patients can access medical history")
        patient = user.patient
        appointments, prescriptions = get_patient_data(patient)
        return Response({
            "patient": user.username,
            "appointments": [
                {
                    "id": a.id,
                    "doctor": a.doctor.user.username,
                    "date": a.date,
                    "time": a.time,
                    "status": a.status
                }
                for a in appointments
            ],

            "prescriptions": [
                {
                    "id": p.id,
                    "doctor": p.doctor.user.username,
                    "medicines": p.medicines,
                    "date": p.created_at
                }
                for p in prescriptions
            ]
        })
        
        
        