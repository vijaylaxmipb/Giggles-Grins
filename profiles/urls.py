from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<str:order_number>/', views.order_history, name='order_history'),
    path('download-invoice/<str:order_number>/', views.download_invoice, name='download_invoice'),  # Use <str:order_number>
]
