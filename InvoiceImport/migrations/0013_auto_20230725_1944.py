# Generated by Django 3.2.19 on 2023-07-25 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0012_alter_invoice_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='purchase_date',
            field=models.DateField(),
        ),
    ]
