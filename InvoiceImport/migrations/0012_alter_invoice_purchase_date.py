# Generated by Django 3.2.19 on 2023-07-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0011_alter_invoice_invoice_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='purchase_date',
            field=models.DateField(null=True),
        ),
    ]