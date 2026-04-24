from .utils import send_appointment_email
from .sms import send_sms


class NotificationService:

    @staticmethod
    def send_email(user, subject, message):
        try:
            send_appointment_email(
                email=user.email,
                message=f"{subject}: {message}"
            )
        except Exception as e:
            print("Email Error:", e)

    @staticmethod
    def send_sms(user, message):
        try:
            if hasattr(user, 'phone_number') and user.phone_number:
                send_sms(
                    to=user.phone_number,
                    message=message
                )
        except Exception as e:
            print("SMS Error:", e)
            
            