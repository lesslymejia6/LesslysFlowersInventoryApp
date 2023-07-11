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

# from .views import home_page, inventory_page, inventory_import, data_charts, month_selection

app_name = 'InvoiceImport'

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^inventory/$', views.import_page, name='inventory'),
    url(r'^upload/$', views.invoice_import, name='upload'),
    # url(r'^graph/$', views.data_charts, name='graph'),
    url(r'^selection/$', views.month_selection_view, name="selection"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
