from django.urls import path
from .views import InvoiceCreateView, InvoiceListView, generate_invoice_pdf

urlpatterns = [
    path('invoice/create/', InvoiceCreateView.as_view()),
    path('invoice/', InvoiceListView.as_view()),
    path('invoice/<int:pk>/pdf/', generate_invoice_pdf),
]



