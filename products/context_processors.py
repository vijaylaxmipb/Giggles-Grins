from .models import Category

def categories_with_subcategories(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return {'categories_with_subcategories': categories}



