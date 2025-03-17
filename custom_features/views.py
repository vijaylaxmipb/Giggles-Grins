from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import FAQ
from .forms import ContactFormModelForm
from django.conf import settings


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'custom_features/faq.html', {'faqs': faqs})


def contact_form_view(request):
    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            form.save()

            # Send confirmation email
            send_mail(
                subject='Thank you for your message!',
                message=f"Dear {form.cleaned_data['name']},\n\nThank you for contacting us. We will get back to you soon.\n\nMessage:\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
                fail_silently=False,
            )

            return redirect('contact_success')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = ContactFormModelForm()

    return render(request, 'custom_features/contact_form.html', {'form': form})