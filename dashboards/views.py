from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from billing.models import Invoice
from labreports.models import LabReport


def home(request):
    if not request.user.is_authenticated:
        return redirect('/api-auth/login/')
    user = request.user
    if user.role == 'doctor':
        return redirect('/doctor/dashboard/')
    elif user.role == 'patient':
        return redirect('/patient/dashboard/')
    elif user.role == 'receptionist':
        return redirect('/receptionist/dashboard/')
    return redirect('/api-auth/login/')



@login_required
def post_login_redirect(request):
    user = request.user
    if user.role == 'doctor':
        return redirect('/doctor/dashboard/')
    elif user.role == 'patient':
        return redirect('/patient/dashboard/')
    elif user.role == 'receptionist':
        return redirect('/receptionist/dashboard/')
    return redirect('/api-auth/login/')



@login_required
def doctor_dashboard(request):
    user = request.user
    if user.role != 'doctor':
        return redirect('/api-auth/login/')
    appointments = Appointment.objects.filter(doctor=user.doctor).order_by('-id')
    invoices = Invoice.objects.filter(appointment__doctor=user.doctor).order_by('-id')
    lab_reports = LabReport.objects.filter(doctor=user.doctor).order_by('-id')
    return render(request, "dashboards/doctor_dashboard.html", {
        "appointments": appointments,
        "invoices": invoices,
        "lab_reports": lab_reports
    })
    



@login_required
def patient_dashboard(request):
    user = request.user
    if user.role != 'patient':
        return redirect('/api-auth/login/')
    appointments = Appointment.objects.filter(patient=user.patient).order_by('-id')
    invoices = Invoice.objects.filter(appointment__patient=user.patient).order_by('-id')
    lab_reports = LabReport.objects.filter(patient=user.patient).order_by('-id')

    return render(request, "dashboards/patient_dashboard.html", {
        "appointments": appointments,
        "invoices": invoices,
        "lab_reports": lab_reports
    })
    



@login_required
def receptionist_dashboard(request):
    user = request.user
    if user.role != 'receptionist':
        return redirect('/api-auth/login/')
    appointments = Appointment.objects.all().order_by('-id')
    invoices = Invoice.objects.all().order_by('-id')
    lab_reports = LabReport.objects.all().order_by('-id')
    return render(request, "dashboards/receptionist_dashboard.html", {
        "appointments": appointments,
        "invoices": invoices,
        "lab_reports": lab_reports
    })




    
