"""FlowersInventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from FlowersInventory import settings
from django.conf.urls.static import static
from . import views

app_name = 'InvoiceImport'

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^import/$', views.import_page, name='import'),
    url(r'^invoices/$', views.invoices_view, name="invoices"),
    url(r'^invoices/products/$', views.invoices_products_view, name='invoice_product'),
    url(r'^inventory/$', views.products_inventory_view, name='inventory'),
    url(r'^inventory/graph/$', views.products_inventory_as_list_view, name='inventory_graph'),
    url(r'^inventory/update/$', views.select_product_to_update, name='select_product_to_update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
