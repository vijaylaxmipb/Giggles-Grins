from django.contrib import admin
from .models import Category, Product, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (

        'friendly_name',
        'name',
    )
    search_fields = ('name', 'friendly_name')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name', 'category')
    search_fields = ('name', 'friendly_name')  
    list_filter = ('category',) 
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'get_subcategory',
        'price',
        'rating',
        'image',
    )
    list_filter = ('category', 'subcategory')  
    search_fields = ('name', 'description', 'sku')
    ordering = ('sku',)

    def get_subcategory(self, obj):
        return obj.subcategory.name if obj.subcategory else "-"
    get_subcategory.short_description = 'Subcategory'  