from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from rest_framework import status
from .models import LabReport
from .serializers import LabReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required


class LabReportCreateView(generics.CreateAPIView):
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'doctor':
            raise PermissionDenied("Only doctor can upload lab reports")
        serializer.save(doctor=user.doctor)


class LabReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            patient = user.patient   # IMPORTANT
        except:
            return Response({"error": "Patient profile not found"}, status=400)
        reports = LabReport.objects.filter(patient=patient)
        serializer = LabReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    

class LabReportListView(generics.ListAPIView):
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return LabReport.objects.all()
        elif user.role == 'patient':
            return LabReport.objects.filter(patient=user.patient)
        return LabReport.objects.none()



@login_required
def download_lab_report(request, pk):
    user = request.user
    try:
        report = LabReport.objects.get(id=pk)
    except LabReport.DoesNotExist:
        raise Http404("Report not found")
    if user.role == 'patient' and report.patient != user.patient:
        raise Http404("Not allowed")
    if user.role == 'doctor' and report.doctor != user.doctor:
        raise Http404("Not allowed")

    return FileResponse(report.report_file, as_attachment=True)


