from django.contrib import admin
from .models import Category, Product, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (

        'friendly_name',
        'name',
    )

   

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name', 'category')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)

