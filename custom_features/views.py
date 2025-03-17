from django.shortcuts import render, redirect
from .models import FAQ
from .forms import ContactFormModelForm


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'custom_features/faq.html', {'faqs': faqs})


def contact_form_view(request):
    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactFormModelForm()

    return render(request, 'custom_features/contact_form.html', {'form': form})
