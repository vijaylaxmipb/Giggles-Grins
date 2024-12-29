from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps

@login_required
def order_tracking(request):
    """
    View to track orders for the logged-in user.
    """
    Order = apps.get_model('orders', 'Order')  # Dynamically fetch the Order model
    orders = Order.objects.filter(user=request.user).order_by('-order_date')  # Get user's orders
    return render(request, 'orders/order_tracking.html', {'orders': orders})