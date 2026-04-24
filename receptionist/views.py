from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsReceptionist
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()


class ReceptionistDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]

    def get(self, request):
        return Response({
            "message": "Welcome Receptionist Dashboard"
        })



class CreatePatientView(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]

    def post(self, request):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response({"error": "Username already exists"})
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            role='patient'
        )
        user.set_password(data['password'])
        user.save()

        return Response({"message": "Patient created successfully"})



class CreateAppointmentByReceptionist(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]

    def post(self, request):
        patient_id = request.data.get('patient_id')
        doctor_id = request.data.get('doctor_id')
        date = request.data.get('date')
        time = request.data.get('time')
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            status='pending'
        )
        return Response({
            "message": "Appointment created",
            "appointment_id": appointment.id
        })



class AllAppointmentsView(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]

    def get(self, request):
        appointments = Appointment.objects.all()
        data = [
            {
                "id": a.id,
                "patient": a.patient.user.username,
                "doctor": a.doctor.user.username,
                "date": a.date,
                "time": a.time,
                "status": a.status
            }
            for a in appointments
        ]
        return Response(data)
    
    
class PatientListView(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]

    def get(self, request):
        patients = Patient.objects.all()
        data = [
            {
                "id": p.id,
                "username": p.user.username,
                "email": p.user.email,
            }
            for p in patients
        ]
        return Response({
            "total_patients": patients.count(),
            "patients": data
        })
        
        
           