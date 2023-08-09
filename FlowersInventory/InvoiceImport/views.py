import json
from django.shortcuts import render
import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import Inventory, Product, Invoice, InvoiceProducts


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

        invoice_object = create_invoice(
            purchase_date=dataframe.purchase_date[0],
            invoice_total=dataframe.invoice_total[0]
        )

        for dataframe_row in dataframe.itertuples():
            # checks for empty cells in each dataframe_row
            if (pd.isnull(dataframe_row.name)) or \
                    (pd.isnull(dataframe_row.unit_type)) or \
                    (pd.isnull(dataframe_row.unit_price)):
                continue

            product_object = add_or_create_product(dataframe_row)

            add_product_to_inventory(dataframe_row, product_object)

            updating_invoice_product_model(dataframe_row, product_object, invoice_object)

        context = {
            'uploaded_file_url': uploaded_file_url,
        }
        return render(request, "import_success.html", context)

    return render(request, 'import_view.html', {})


def create_invoice(purchase_date, invoice_total):
    invoice_obj = Invoice.objects.create(purchase_date=purchase_date,
                                         invoice_total=invoice_total)

    invoice_obj.save()

    return invoice_obj


def add_or_create_product(dataframe_row):
    # Check if product exists, if not create it
    product_obj, created = Product.objects.get_or_create(name=dataframe_row.name,
                                                         unit_type=dataframe_row.unit_type,
                                                         unit_price=dataframe_row.unit_price)

    return product_obj


def updating_invoice_product_model(dataframe_row, product_object, invoice_object):
    # updating InvoiceProducts model
    total_units = dataframe_row.total_units
    invoice_product = InvoiceProducts(
        product=product_object,
        invoice=invoice_object,
        total_units=total_units
    )
    invoice_product.save()


def add_product_to_inventory(dataframe_row, product_object):
    # Add product to inventory
    inventory_obj, created = Inventory.objects.get_or_create(product=product_object)
    inventory_obj.total_units += dataframe_row.total_units
    inventory_obj.save()


def invoices_view(request):
    month_str = request.GET.get('monthSelect', None)
    if month_str is not None:
        month_int = int(month_str)

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

    context = {
        'invoice': invoice,
        'invoices_products': invoices_products,
        # 'product_inventory': product_inventory
    }

    # SET UP VIEWS AND MANIPULATE DATA
    return render(request, "invoice_product_view.html", context)


def inventory_view(request):
    products = Inventory.objects.all()

    context = {
        # 'product_inventory': product_inventory,
        'products': products
    }

    return render(request, "inventory_view.html", context)


def inventory_graph(request):
    labels = []
    data = []

    queryset = Inventory.objects.order_by('total_units')

    for inventory in queryset:
        labels.append(inventory.product.name)
        data.append(inventory.total_units)

    context = {
        "labels": json.dumps(labels),
        "data": json.dumps(data),
    }
    return render(request, "inventory_graph.html", context)


def select_product_to_update(request):
    inventory_queryset = Inventory.objects.all()
    used_inventory = request.POST.get('usedInventory', None)
    inventory_id = request.POST.get('inventoryId', None)

    if inventory_id and used_inventory:
        check_if_inventory_has_enough_units(used_inventory, inventory_id)

    context = {
        'inventory_queryset': inventory_queryset
    }
    return render(request, "inventory_update_view.html", context)


def check_if_inventory_has_enough_units(used_inventory, inventory_id):
    inventory_instance = Inventory.objects.get(id=inventory_id)
    total_units_available = inventory_instance.total_units
    # Check if inventory has enough else raise exception
    if total_units_available >= int(used_inventory):
        inventory_instance.total_units = inventory_instance.total_units - int(used_inventory)
    else:
        raise ValueError("Not enough inventory to use")

    inventory_instance.save()
