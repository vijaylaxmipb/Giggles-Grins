from django.shortcuts import render, redirect
from django.contrib import messages  
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.warning(request, "This email is already subscribed.")
            return redirect('home')
    else:
        form = NewsletterSignupForm()
    return render(request, 'newsletter/signup.html', {'form': form})

