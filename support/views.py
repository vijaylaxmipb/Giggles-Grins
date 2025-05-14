
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import FAQ
from .forms import ContactFormModelForm
from django.conf import settings
from django.contrib import messages


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'support/faq.html', {'faqs': faqs})


def contact_form_view(request):
    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                send_mail(
                    subject='Thank you for your message!',
                    message=(
                        f"Dear {form.cleaned_data['name']},\n\n"
                        "Thank you for contacting us. We will get back to you soon.\n\n"
                        f"Message:\n{form.cleaned_data['message']}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[form.cleaned_data['email']],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                print(f"Email sending failed: {e}")
                messages.error(request, "Your message was saved, but the confirmation email couldn't be sent.")

            return redirect('contact_success')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ContactFormModelForm()

    return render(request, 'support/contact_form.html', {'form': form})


def contact_success(request):
    return render(request, 'support/contact_success.html')