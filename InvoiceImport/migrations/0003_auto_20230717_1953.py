# Generated by Django 3.2.19 on 2023-07-17 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0002_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]
