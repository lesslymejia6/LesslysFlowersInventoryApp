from django.db import models

UNIT_TYPE_CHOICES = (
    ('bunch', 'Bunch'),
    ('stem', 'Stem')
)


class Invoice(models.Model):
    purchase_date       = models.DateField(auto_now=False, auto_now_add=False)
    invoice_total       = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Purchase date: " + str(self.purchase_date)


class Product(models.Model):
    name            = models.CharField(max_length=300)
    unit_type       = models.CharField(max_length=50, default='bunch', choices=UNIT_TYPE_CHOICES)
    unit_price      = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class InvoiceProducts(models.Model):
    product         = models.ForeignKey("InvoiceImport.Product", on_delete=models.CASCADE)
    invoice         = models.ForeignKey("InvoiceImport.Invoice", on_delete=models.CASCADE)
    total_units     = models.IntegerField(default=0)


class Inventory(models.Model):
    product             = models.ForeignKey("InvoiceImport.Product", on_delete=models.CASCADE)
    total_units         = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + "-" + str(self.total_units)
