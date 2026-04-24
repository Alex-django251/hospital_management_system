from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Invoice
from .serializers import InvoiceSerializer
from services.billing_service import BillingService
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Invoice


class InvoiceCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'doctor':
            raise PermissionDenied("Only doctor can create invoice")
        appointment = serializer.validated_data['appointment']
        invoice = BillingService.generate_invoice(appointment)
        return invoice
    
    
class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Invoice.objects.all()
        elif user.role == 'patient':
            return Invoice.objects.filter(
                appointment__patient=user.patient
            )
        return Invoice.objects.none()
    
    
def generate_invoice_pdf(request, pk):
    try:
        invoice = Invoice.objects.get(id=pk)
    except Invoice.DoesNotExist:
        return HttpResponse("Invoice not found", status=404)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{pk}.pdf"'
    p = canvas.Canvas(response)
    y = 800
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "Hospital Invoice")
    y -= 40
    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Invoice ID: {invoice.id}")
    y -= 20
    p.drawString(100, y, f"Patient: {invoice.appointment.patient.user.username}")
    y -= 20
    p.drawString(100, y, f"Doctor: {invoice.appointment.doctor.user.username}")
    y -= 20
    p.drawString(100, y, f"Date: {invoice.created_at}")
    y -= 40
    p.drawString(100, y, f"Consultation Fee: {invoice.consultation_fee}")
    y -= 20
    p.drawString(100, y, f"Medicine Charges: {invoice.medicine_charges}")
    y -= 20
    p.drawString(100, y, f"Lab Charges: {invoice.lab_charges}")
    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, f"Total Amount: {invoice.total_amount}")
    y -= 50
    p.setFont("Helvetica", 10)
    p.drawString(100, y, "Thank you for visiting our hospital.")
    p.showPage()
    p.save()
    return response


