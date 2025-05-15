from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.messages.api import get_messages
from products.models import Product
from django.http import JsonResponse


# Create your views here.
def view_bag(request):
    storage = get_messages(request)
    for message in storage:
        print(f"Message: {message}")

    return render(request, 'bag/bag.html')


@require_POST
def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(
                    request,
                    f'Updated size {
                        size.upper()} {
                        product.name} quantity to {
                        bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(
                    request, f'Added size {
                        size.upper()} {
                        product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(
                request, f'Added size {
                    size.upper()} {
                    product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(
                request, f'Updated {
                    product.name} quantity to {
                    bag[item_id]}')

        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(
                request,
                f'Updated size {
                    size.upper()} {
                    product.name} quantity to {
                    bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request, f'Removed size {
                    size.upper()} {
                    product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(
                request, f'Updated {
                    product.name} quantity to {
                    bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    try:
        print("POST DATA:", request.POST)
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size')
        bag = request.session.get('bag', {})

        if size:
            if item_id in bag and size in bag[item_id].get('items_by_size', {}):
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
            else:
                print("❗Item/Size not found in bag")
                return JsonResponse({'error': 'Item or size not found'}, status=400)
        else:
            if item_id in bag:
                bag.pop(item_id)
                messages.success(request, f'Removed {product.name} from your bag')
            else:
                print("❗Item not found in bag")
                return JsonResponse({'error': 'Item not found'}, status=400)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        print("❌ Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)


def session_test(request):
    request.session['test'] = 'Session is working!'
    return HttpResponse('Session test completed.')
