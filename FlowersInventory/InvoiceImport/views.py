from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from django.views.generic.list import ListView
from collections import Counter
from django.core.files.storage import FileSystemStorage
from .models import Inventory, Product, Invoice, InvoiceProducts
from tablib import Dataset
from .resources import InvoiceResource
from django.views.decorators.csrf import csrf_exempt


def home_page(request):
    greeting = 'HIIIII '
    context = {
        'greeting': greeting
    }
    return render(request, "home.html", context)


def import_page(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        dataframe = pd.read_excel(filename, engine='openpyxl')

        # Create invoice for record keeping
        invoice_obj = Invoice.objects.create(purchase_date=dataframe.purchase_date[0],
                                             invoice_total=dataframe.invoice_total[0])
        invoice_obj.save()

        #
        for dataframe_row in dataframe.itertuples():
            # checks for empty cells in each dataframe_row
            if (pd.isnull(dataframe_row.name)) or \
                    (pd.isnull(dataframe_row.unit_type)) or \
                    (pd.isnull(dataframe_row.unit_price)):
                continue

            # Check if product exists, if not create it
            product_obj, created = Product.objects.get_or_create(name=dataframe_row.name,
                                                                 unit_type=dataframe_row.unit_type,
                                                                 unit_price=dataframe_row.unit_price)

            # Add product to inventory
            inventory_obj, created = Inventory.objects.get_or_create(product=product_obj)
            inventory_obj.total_units += dataframe_row.total_units
            inventory_obj.save()

            # updating InvoiceProducts model
            total_units = dataframe_row.total_units
            invoice_product = InvoiceProducts(
                product=product_obj,
                invoice=invoice_obj,
                total_units=total_units
            )
            invoice_product.save()

        context = {
            'uploaded_file_url': uploaded_file_url,
        }
        return render(request, "import_success.html", context)

    return render(request, 'import_view.html', {})


def invoice_import(request):
    if request.method == 'POST':
        InvoiceResource()
        dataset = Dataset()
        new_invoice = request.FILES['myfile']
        data_import = dataset.load(new_invoice.read())
        result = InvoiceResource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            InvoiceResource.import_data(dataset, dry_run=False)
    return render(request, 'import_success.html', {})


def invoices_view(request):
    month_str = request.GET.get('monthSelect', None)
    if month_str is not None:
        print(type(month_str))
        month_int = int(month_str)
        print(type(month_int))

        # filter by the month
        invoices_qs = Invoice.objects.filter(
            purchase_date__month__lte=month_int,
            purchase_date__month__gte=month_int
        )
    else:
        invoices_qs = Invoice.objects.none()

    return render(request, "invoices_view.html", {'invoices': invoices_qs})


def invoices_products_view(request):
    invoice_id = request.GET.get('invoice_id', None)
    invoice = Invoice.objects.get(id=invoice_id)

    # product_inventory = []
    if invoice_id is not None:

        invoices_products = InvoiceProducts.objects.filter(invoice_id=invoice_id)

    else:
        invoices_products = InvoiceProducts.objects.none()

    # print(product_inventory)
    context = {
        'invoice': invoice,
        'invoices_products': invoices_products,
        # 'product_inventory': product_inventory
    }

    # SET UP VIEWS AND MANIPULATE DATA
    return render(request, "invoice_product_view.html", context)


def inventory(request):
    products = Inventory.objects.all()
    # MAYBE THIS CAN BE ITS OWN VIEW -- HOW MANY DO I HAVE OF ____?
    # invoice_id = request.GET.get('invoice_id', None)
    # product_inventory = []
    # invoices_products = InvoiceProducts.objects.filter(invoice_id=invoice_id)
    #
    # for invoices_product in invoices_products:
    #     product = invoices_product.product
    #     product_inventory_entry = Inventory.objects.get(product=product)
    #     product_inventory.append(product_inventory_entry)

    context = {
        # 'product_inventory': product_inventory,
        'products': products
    }

    return render(request, "inventory_view.html", context)
