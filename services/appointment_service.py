from appointments.models import Appointment

class AppointmentService:

    @staticmethod
    def create_appointment(patient, doctor, date, time):
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            status='pending'
        )
        return appointment
    
    