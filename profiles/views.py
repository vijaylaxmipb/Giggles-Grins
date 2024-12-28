from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from orders.models import Order, OrderLineItem
from checkout.models import Order
from django.http import HttpResponse
from orders.models import Order 

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def download_invoice(request, order_id):
    # Get the order by order ID
    order = get_object_or_404(Order, id=order_id)

    # Generate invoice content
    invoice_content = f"""
    Invoice for Order #{order.id}
    Date: {order.order_date}
    Total: ${order.total_price}

    Items in the order:
    """
    for item in order.lineitems.all():
        invoice_content += f"\n- {item.product_name} x{item.quantity} - ${item.lineitem_total}"

    response = HttpResponse(invoice_content, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename=invoice_{order.id}.txt"
    return response