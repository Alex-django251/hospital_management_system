class NotificationService:

    @staticmethod
    def send_email(user, subject, message):
        print(f"Email sent to {user.email}: {subject}")

    @staticmethod
    def send_sms(user, message):
        print(f"SMS sent to {user.phone}: {message}")
        
        