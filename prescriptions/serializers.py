from rest_framework import serializers
from .models import Prescription, Appointment

class PrescriptionSerializer(serializers.ModelSerializer):
    appointment_id = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(),
        source='appointment',
        write_only=True
    )
    appointment = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'
        
        