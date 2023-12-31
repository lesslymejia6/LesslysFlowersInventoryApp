import json
from django.shortcuts import render
import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import Product, Invoice, InvoiceProducts


def home_page(request):
    greeting = 'HIIIII '
    context = get_products_inventory()
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
    product_obj, created = Product.objects.get_or_create(name=dataframe_row.name, unit_type=dataframe_row.unit_type,
                                                         unit_price=dataframe_row.unit_price)

    available_total_units = product_obj.total_units

    product_obj.total_units = available_total_units + dataframe_row.total_units

    product_obj.save()

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

    invoices_products = get_invoice_products_as_list_view(invoice_id)

    context = {
        'invoice': invoice,
        'invoices_products': invoices_products,
        # 'product_inventory': product_inventory
    }

    # SET UP VIEWS AND MANIPULATE DATA
    return render(request, "invoice_product_view.html", context)


def get_invoice_products_as_list_view(invoice_id):
    if invoice_id is not None:

        invoices_products = InvoiceProducts.objects.filter(invoice_id=invoice_id)

    else:
        invoices_products = InvoiceProducts.objects.none()

    return invoices_products


def products_inventory_view(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, "inventory_view.html", context)


def products_inventory_as_list_view(request):
    context = get_products_inventory()
    # print(context)
    return render(request, "inventory_graph.html", context)


def get_products_inventory():
    product_names = []
    product_total_units = []

    queryset = Product.objects.order_by('total_units')

    for product in queryset:
        product_names.append(product.name)
        product_total_units.append(product.total_units)

    payload = {
        "product_names": json.dumps(product_names),
        "product_total_units": json.dumps(product_total_units),
    }

    return payload


def select_product_to_update(request):
    products_queryset = Product.objects.all()
    used_product = request.POST.get('usedInventory', None)
    product_id = request.POST.get('productId', None)

    if product_id and used_product:
        check_if_inventory_has_enough_units(used_product, product_id)

    context = {
        'products_queryset': products_queryset
    }
    return render(request, "inventory_update_view.html", context)


def check_if_inventory_has_enough_units(used_product, product_id):
    product_instance = Product.objects.get(id=product_id)
    total_units_available = product_instance.total_units
    # Check if inventory has enough else raise exception
    if total_units_available >= int(used_product):
        product_instance.total_units = product_instance.total_units - int(used_product)
    else:
        raise ValueError("Not enough inventory to use")

    product_instance.save()
