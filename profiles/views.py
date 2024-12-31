from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from orders.models import UserOrder, OrderDetail
from django.http import HttpResponse
from checkout.models import Order



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

    #orders = UserOrder.objects.filter(user=request.user).order_by('-order_date')
    orders = profile.orders.all().order_by('-date')
    

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)
    

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user_profile__user=request.user)
    messages.info(request, (
        f'This is a past confirmation for order number {order.order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def download_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user_profile__user=request.user)

    invoice_content = f"""
    ===========================
             INVOICE
    ===========================
    Invoice for Order: #{order.order_number}
    Date: {order.date.strftime('%B %d, %Y, %I:%M %p')}
    ===========================

    Total: ${order.grand_total}

    Delivery Details:
    ---------------------------
    Name: {order.full_name}
    Address: {order.street_address1}, {order.street_address2 or ''}
    City: {order.town_or_city}
    County: {order.county}
    Country: {order.country}
    Postal Code: {order.postcode}
    Phone: {order.phone_number}
    ---------------------------

    Items in the Order:
    ---------------------------
    """
    for item in order.lineitems.all():
        invoice_content += f"- {item.product.name} x{item.quantity} - ${item.lineitem_total}\n"

    invoice_content += """
    ===========================
    Thank you for shopping with us!
    Visit us again at Giggles & Grins.
    ===========================
    """

    response = HttpResponse(invoice_content, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename=invoice_{order.order_number}.txt"
    return response
