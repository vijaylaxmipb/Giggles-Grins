from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<int:order_id>/', views.order_history, name='order_history'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),    
]