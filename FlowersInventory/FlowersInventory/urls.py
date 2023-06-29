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
from django.contrib import admin
from FlowersInventory import settings
from django.conf.urls.static import static
from django.urls import path, include
# from InvoiceImport.views import home_page, inventory_page, inventory_import, data_charts, month_selection


urlpatterns = [

    # path(r'^$', home_page, name='home'),
    # path(r'^inventory/', inventory_page, name='inventory'),
    # path(r'^imported/', inventory_import, name='import'),
    # path(r'^graph/', data_charts, name='graph'),
    # path(r'^selection/', month_selection, name="selection"),
    path('', include('InvoiceImport.urls', namespace="import")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
