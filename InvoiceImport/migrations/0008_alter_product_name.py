# Generated by Django 3.2.19 on 2023-07-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0007_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
