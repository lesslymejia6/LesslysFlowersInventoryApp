from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from django.views.generic.list import ListView
from collections import Counter
from django.core.files.storage import FileSystemStorage
from .models import Inventory, Product, Invoice,InvoiceProducts
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
        empExcelData = pd.read_excel(filename, engine='openpyxl')
        dbframe = empExcelData

        # Create invoice for record keeping
        invoice_obj = Invoice.objects.create(purchase_date=dbframe.purchase_date[0],
                                             invoice_total=dbframe.invoice_total[0])
        invoice_obj.save()

        for dbframe in dbframe.itertuples():
            # Check if product exists, if not create it
            product_obj, created = Product.objects.get_or_create(name=dbframe.name, unit_type=dbframe.unit_type,
                                                                 unit_price=dbframe.unit_price)

            # Add product to inventory
            inventory_obj, created = Inventory.objects.get_or_create(product=product_obj,
                                                                     total_units=dbframe.total_units)
            inventory_obj.total_units += dbframe.total_units
            inventory_obj.save()

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
    month_str = request.GET.get('month', None)
    year_str = request.GET.get('year', None)
    if month_str is not None:
        print(type(month_str))
        month_int = int(month_str)
        print(type(month_int))

        # filter by the month
        invoices_qs = Invoice.objects.filter(
            purchase_date__month__lte=month_int,
            purchase_date__month__gte=month_int
        )

    elif year_str is not None:
        print(type(month_str))
        month_int = int(month_str)
        print(type(month_int))

        # filter by the month
        invoices_qs = Invoice.objects.filter(
            purchase_date__year__lte=month_int,
            purchase_date__year__gte=month_int
        )
    else:
        invoices_qs = Invoice.objects.none()

    return render(request, "invoices_view.html", {'invoices': invoices_qs})


def invoices_products_view(request):
    invoice_id = request.GET.get('invoice_id', None)

    if invoice_id is not None:

        # invoice_id = Invoice.objects.filter(id=invoice_id)

        invoice_products = InvoiceProducts.objects.filter(invoice_id=invoice_id)

    else:
        invoice_products = InvoiceProducts.objects.none()

    context = {
        'invoice_id': invoice_id,
        'invoice_products': invoice_products
    }

    # SET UP VIEWS AND MANIPULATE DATA
    return render(request, "invoices_view.html", context)
