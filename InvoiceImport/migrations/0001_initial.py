# Generated by Django 3.2.19 on 2023-07-11 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('unit_type', models.CharField(choices=[('bunch', 'Bunch'), ('stem', 'Stem')], default='bunch', max_length=50)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvoiceImport.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvoiceImport.product')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='products',
            field=models.ManyToManyField(through='InvoiceImport.InvoiceProducts', to='InvoiceImport.Product'),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_units', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvoiceImport.product')),
            ],
        ),
    ]
