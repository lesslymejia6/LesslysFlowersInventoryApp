from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
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


def inventory_page(request):
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
                                                 unit_type=dbframe.unit_type, total_units=dbframe.total_units,
                                                 unit_price=dbframe.unit_price, total=dbframe.total)
            invoice_obj.save()

            # Add product to inventory
            inventory_obj, created = Inventory.objects.get_or_create(product=product_obj)
            inventory_obj.total_units += dbframe.total_units
            inventory_obj.save()

        context = {
            'uploaded_file_url': uploaded_file_url,
        }
        return render(request, "import_success.html", context)
    return render(request, 'inventory.html', {})


def inventory_import(request):
    if request.method == 'POST':
        InvoiceResource()
        dataset = Dataset()
        new_invoice = request.FILES['myfile']
        data_import = dataset.load(new_invoice.read())
        result = InvoiceResource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            InvoiceResource.import_data(dataset, dry_run=False)
    return render(request, 'import_success.html', {})


@csrf_exempt
def month_selection(request):
    purchase_date = request.POST.get('purchase_date')

    if purchase_date is not None:
        print("got it")
        found = True
    else:
        print("try again!")
        found = False

        if request.is_ajax():
            print("ajax request")
            json_data = {
                "found": found,
            }

            return JsonResponse(json_data)

    return render(request, "selection.html", {})


def data_charts(request):
    inventory = Inventory.objects.order_by('product')

    data = Counter()
    for row in inventory:
        yymm = row.product
        data[yymm] += 1

    labels, values = zip(*data.items())

    context = {
        "labels": labels,
        "values": values,
    }

    return render(request, "graph.html", context)
