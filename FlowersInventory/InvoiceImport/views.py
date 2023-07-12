from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from django.views.generic.list import ListView
from collections import Counter
from django.core.files.storage import FileSystemStorage
from .models import Inventory, Product, Invoice
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
        for dbframe in dbframe.itertuples():
            # Check if product exists, if not create it
            product_obj, created = Product.objects.get_or_create(name=dbframe.name, unit_price=dbframe.unit_price)
            # Create invoice for record keeping
            invoice_obj = Invoice.objects.create(product=product_obj, purchase_date=dbframe.purchase_date,
                                                 total=dbframe.total)
            invoice_obj.save()

            # Add product to inventory
            inventory_obj, created = Inventory.objects.get_or_create(product=product_obj)
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


def month_selection_view(request):
    month_integer = request.GET.get('month')
    month_integer = int(month_integer)
    # filter by the month
    invoices_qs = Invoice.objects.filter(
        purchase_date__month__lte=month_integer,
        purchase_date__month__gte=month_integer
    )


    #
    # context = {
    #     'invoice_list': queryset
    # }
    # # if request.method == 'GET':
    # #     invoices = ListView(Invoice.objects.get(name=Invoice.products))
    # #     return JsonResponse({'context': invoices})
    # # else:
    # #     return JsonResponse({'status': 'INVALID!'})
    return render(request, "month_selection_view.html", {'invoices': invoices_qs})
