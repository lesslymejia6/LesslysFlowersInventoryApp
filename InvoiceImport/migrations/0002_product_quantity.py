# Generated by Django 3.2.19 on 2023-07-12 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]