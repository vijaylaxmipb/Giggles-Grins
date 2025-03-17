from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # You can send an email here or log the data
            print(f"Message from {name} ({email}): {message}")

            # Show a success message
            messages.success(
                request, 'Thank you for contacting us! We will get back to you soon.')
            form = ContactForm()  # Clear the form after submission
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})

