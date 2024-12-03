#from django.shortcuts import render

# Create your views here.

#def index(request):
""" A view to return the index page """

   # return render(request, 'home/index.html')

#def profile(request):
    #return render(request, 'profile.html')

from django.shortcuts import render
from products.models import Category

# Create your views here.

def index(request):
    """ A view to return the index page """
    categories = Category.objects.all()  # Fetch categories from the database
    context = {
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'home/index.html', context)


def profile(request):
    """ A view to return the profile page """
    categories = Category.objects.all()  # Fetch categories from the database
    context = {
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'profile.html', context)
