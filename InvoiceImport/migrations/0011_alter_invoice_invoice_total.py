# Generated by Django 3.2.19 on 2023-07-21 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0010_rename_total_invoice_invoice_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, null=True),
        ),
    ]
