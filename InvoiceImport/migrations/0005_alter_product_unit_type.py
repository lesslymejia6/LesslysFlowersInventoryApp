# Generated by Django 3.2.19 on 2023-07-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceImport', '0004_auto_20230720_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit_type',
            field=models.CharField(choices=[('bunch', 'Bunch'), ('stem', 'Stem')], default='bunch', max_length=50, null=True),
        ),
    ]
