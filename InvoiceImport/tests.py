from django.test import TestCase
from .models import Invoice, Product, InvoiceProducts
import pandas as pd
from decimal import Decimal
from datetime import date

from .views import create_invoice, add_or_create_product, updating_invoice_product_model, \
    check_if_inventory_has_enough_units


# Create your tests here.


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_invoices(self):
        # ARRANGE
        # create dataframe
        purchase_date = date(2022, 4, 23)

        invoice_total = Decimal('12.99')

        # ACT
        create_invoice(purchase_date, invoice_total)
        # ASSERT
        # get invoice by date and assert it exists

        invoices_qs = Invoice.objects.all()

        first_invoice_qs = invoices_qs.filter(
            purchase_date=purchase_date
        )

        self.assertEquals(
            invoices_qs.count(), 1
        )
        single_invoice = first_invoice_qs.get()
        self.assertEquals(
            single_invoice.purchase_date, purchase_date
        )

        self.assertEquals(
            single_invoice.invoice_total, invoice_total
        )

    def test_add_or_create_product(self):
        # ARRANGE
        name = 'peonies'
        unit_type = 'bunch'
        unit_price = Decimal('18.56')
        total_units = 3

        d = {
            'name': [name],
            'unit_type': [unit_type],
            'unit_price': [unit_price],
            'total_units': [total_units]
        }
        dataframe = pd.DataFrame(data=d)
        # ACT
        for dataframe_row in dataframe.itertuples():
            add_or_create_product(dataframe_row)
        # ASSERT
        products_qs = Product.objects.all()

        first_product_qs = products_qs.filter(
            name=name
        )

        self.assertEquals(
            products_qs.count(), 1
        )

        single_product = first_product_qs.get()
        self.assertEquals(
            single_product.name, name
        )
        self.assertEquals(
            single_product.unit_type, unit_type
        )
        self.assertEquals(
            single_product.unit_price, unit_price
        )

    def test_updating_invoice_product_model(self):
        # ARRANGE
        total_units = 5

        d = {
            'total_units': [total_units],
        }
        dataframe = pd.DataFrame(data=d)

        product_object = Product(name='roses', unit_type='bunch', unit_price=24.99)
        product_object.save()

        invoice_object = Invoice(purchase_date='2022-03-22', invoice_total=34.99)
        invoice_object.save()

        # ACT
        for dataframe_row in dataframe.itertuples():
            updating_invoice_product_model(dataframe_row, product_object, invoice_object)

        # ASSERT
        invoice_product_qs = InvoiceProducts.objects.all()

        first_invoice_product_qs = invoice_product_qs.filter(
            product=product_object
        )

        self.assertEquals(
            invoice_product_qs.count(), 1
        )

        single_invoice_product = first_invoice_product_qs.get()

        self.assertEquals(
            single_invoice_product.product, product_object
        )

        self.assertEquals(
            single_invoice_product.invoice, invoice_object
        )
        self.assertEquals(
            single_invoice_product.total_units, total_units
        )

    def test_check_if_inventory_has_enough_units(self):
        # ARRANGE
        inventory_id = 1
        used_inventory = 2
        used_inventory_gt_available_inventory = 7

        product_object = Product(name='roses', unit_type='bunch', unit_price=24.99, total_units=5)
        product_object.save()

        # ACT
        if inventory_id and used_inventory:
            check_if_inventory_has_enough_units(used_inventory, inventory_id)

        # ASSERT
        inventory_qs = Product.objects.all()

        first_inventory_qs = inventory_qs.filter(
            id=inventory_id
        )

        self.assertEquals(
            inventory_qs.count(), 1
        )

        single_inventory = first_inventory_qs.get()

        self.assertGreaterEqual(
            single_inventory.total_units, used_inventory,
            print(True)

        )

        self.assertLessEqual(
            single_inventory.total_units, used_inventory_gt_available_inventory,
            print(True)
        )