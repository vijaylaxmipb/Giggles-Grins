from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.products_by_category, name='category_products'),
    path('subcategory/<str:subcategory_name>/', views.products_by_subcategory, name='products_by_subcategory'),
    
]