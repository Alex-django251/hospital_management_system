from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    print(f"SMS sent to {to}: {message}")
    
    
        