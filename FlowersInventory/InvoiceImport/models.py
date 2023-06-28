from django.db import models

UNIT_TYPE_CHOICES = (
    ('bunch', 'Bunch'),
    ('stem', 'Stem')
)


class Invoice(models.Model):
    product = models.ForeignKey("InvoiceImport.Product", on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    unit_type = models.CharField(max_length=50, default='bunch', choices=UNIT_TYPE_CHOICES)
    total_units = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Product(models.Model):
    name = models.CharField(max_length=300, unique=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.ForeignKey("InvoiceImport.Product", on_delete=models.CASCADE)
    total_units = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + "-" + str(self.total_units)