from django.urls import path
from . import views

urlpatterns = [
    path('order_tracking/', views.order_tracking, name='order_tracking'),
]
