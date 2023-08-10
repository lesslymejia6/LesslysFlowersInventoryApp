from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver

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
    total_units     = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class InvoiceProducts(models.Model):
    product         = models.ForeignKey("InvoiceImport.Product", on_delete=models.CASCADE)
    invoice         = models.ForeignKey("InvoiceImport.Invoice", on_delete=models.CASCADE)
    total_units     = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + "-" + str(self.total_units)

#
# @receiver(pre_save, sender=InvoiceProducts)
# def calculate_invoice_total(sender, instance, action, *args, **kwargs):
#     if action == 'post_add':
#         invoiceProducts = instance.invoiceProducts.all()
#         unit_prices = Product.objects.all()
#         invoice_total = 0
#         for x in invoiceProducts:
#             invoice_total += x.total_units

