from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Subcategory

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    current_categories = None
    current_subcategories = None
    sort = None
    direction = None
    

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'name'
            elif sortkey == 'category':
                sortkey = 'category__name'
            elif sortkey == 'price':
                sortkey = 'price'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            current_categories = request.GET['category'].split(',')
            pproducts = products.filter(category__name__in=[cat.strip() for cat in current_categories])
            

        if 'subcategory' in request.GET:
            current_subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=[sub.strip() for sub in current_subcategories])

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect('products')

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'all_categories': categories,
        'all_subcategories': subcategories,
        'current_categories': current_categories,
        'current_subcategories': current_subcategories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def products_by_category(request, category_name):
    """ View to display products filtered by category """
    try:
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)

        context = {
            'products': products,
            'current_category': category,
        }
        return render(request, 'products/products.html', context)

    except Category.DoesNotExist:
        messages.error(request, "The selected category does not exist.")
        return redirect('products')


def products_by_subcategory(request, subcategory_name):
    """ View to display products filtered by subcategory """
    try:
        subcategory = Subcategory.objects.get(name=subcategory_name)
        products = Product.objects.filter(category__subcategories=subcategory)

        context = {
            'products': products,
            'current_subcategory': subcategory,
        }
        return render(request, 'products/products_by_subcategory.html', context)

    except Subcategory.DoesNotExist:
        messages.error(request, "The selected subcategory does not exist.")
        return redirect('products')


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)