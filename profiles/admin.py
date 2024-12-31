import importlib
from django.contrib import admin


UserOrder = importlib.import_module('orders.models').UserOrder
OrderDetail = importlib.import_module('orders.models').OrderDetail

admin.site.register(UserOrder)
admin.site.register(OrderDetail)
