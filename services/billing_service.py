from billing.models import Invoice

class BillingService:

    @staticmethod
    def generate_invoice(appointment):
        # 💡 simple business logic (you can expand later)
        consultation_fee = 1000
        medicine_charges = 500
        lab_charges = 300

        total = consultation_fee + medicine_charges + lab_charges

        # 🟢 SAVE IN DATABASE (IMPORTANT FIX)
        invoice = Invoice.objects.create(
            appointment=appointment,
            consultation_fee=consultation_fee,
            medicine_charges=medicine_charges,
            lab_charges=lab_charges,
            total_amount=total
        )

        return invoice