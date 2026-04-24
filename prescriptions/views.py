from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied
from datetime import date
from .models import Prescription
from appointments.models import Appointment
from .serializers import PrescriptionSerializer
from .permissions import IsDoctor



class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'
    
    
class PrescriptionCreateView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'doctor':
            raise PermissionDenied("Only doctors can create prescription")
        serializer.save(doctor=user.doctor)


class PrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Prescription.objects.filter(doctor=user.doctor)
        elif user.role == 'patient':
            return Prescription.objects.filter(patient=user.patient)
        return Prescription.objects.all()



class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'patient':
            raise PermissionDenied("Only patients can access profile")
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "patient_id": getattr(user.patient, "id", None),
        })



class PatientReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'patient':
            raise PermissionDenied("Only patients can access report")
        patient = user.patient
        appointments = Appointment.objects.filter(patient=patient)
        prescriptions = Prescription.objects.filter(patient=patient)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="patient_report.pdf"'
        pdf = canvas.Canvas(response)
        y = 800
        pdf.drawString(100, y, f"Patient Report: {user.username}")
        y -= 30
        pdf.drawString(100, y, f"Email: {user.email}")
        y -= 40
        pdf.drawString(100, y, "Appointments:")
        y -= 20
        for a in appointments:
            pdf.drawString(120, y, f"{a.date} | {a.doctor.user.username} | {a.status}")
            y -= 20
        y -= 20
        pdf.drawString(100, y, "Prescriptions:")
        y -= 20
        for p in prescriptions:
            pdf.drawString(120, y, f"{p.medicines} | {p.created_at}")
            y -= 20
        pdf.showPage()
        pdf.save()
        return response



class PrescriptionPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            prescription = Prescription.objects.get(id=pk)
        except Prescription.DoesNotExist:
            return HttpResponse("Not found", status=404)
        if user.role == 'doctor' and prescription.doctor != user.doctor:
            raise PermissionDenied("Not your prescription")
        if user.role == 'patient' and prescription.patient != user.patient:
            raise PermissionDenied("Not your prescription")
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="prescription_{pk}.pdf"'
        pdf = canvas.Canvas(response)
        y = 800
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, y, "Hospital Prescription")
        y -= 40
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, y, f"Doctor: {prescription.doctor.user.username}")
        y -= 20
        pdf.drawString(100, y, f"Patient: {prescription.patient.user.username}")
        y -= 20
        pdf.drawString(100, y, f"Date: {prescription.created_at}")
        y -= 30
        pdf.drawString(100, y, "Medicines:")
        y -= 20
        pdf.drawString(120, y, prescription.medicines)
        y -= 40
        pdf.drawString(100, y, "Thank you.")
        pdf.showPage()
        pdf.save()
        return response
    
    
    
    