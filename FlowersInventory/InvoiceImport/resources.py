import resources
from .models import Invoice


class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice
