from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Subcategory, Review
from django.db.models.functions import Lower
from .forms import ReviewForm
from .forms import ProductForm
from django.urls import reverse
from .models import Order


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
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
           

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            current_categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=[cat.strip() for cat in current_categories])
            categories = Category.objects.filter(name__in=categories)

            

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
    reviews = product.reviews.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Failed to submit your review. Please check the form.')


    context = {
        'product': product,
        'current_categories': Category.objects.all(),
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home')) 

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))



@login_required
def order_tracking(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_tracking.html', {'orders': orders})