from django.shortcuts import render
from checkout.models import Order

def order_tracking(request):
    
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'orders/order_tracking.html', {'orders': orders})


