from django.contrib import admin
from .models import Category, Product, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name', 'category')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating')
