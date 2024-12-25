from django.shortcuts import render
from checkout.models import Order

def order_tracking(request):
    # Fetch orders linked to the logged-in user
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'orders/order_tracking.html', {'orders': orders})


