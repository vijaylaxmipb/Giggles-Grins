import importlib
from django.contrib import admin

Order = importlib.import_module('orders.models').Order
OrderLineItem = importlib.import_module('orders.models').OrderLineItem

admin.site.register(Order)
admin.site.register(OrderLineItem)
