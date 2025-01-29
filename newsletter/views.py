from django.shortcuts import render, redirect
from django.contrib import messages  
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber

signer = TimestampSigner()


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                token = signer.sign(email)
                confirm_url = request.build_absolute_uri(
                    reverse('newsletter_confirm', args=[urlsafe_base64_encode(force_bytes(email)), token])
                )

                # Send confirmation email
                send_mail(
                    'Confirm Your Subscription',
                    f'Click the link to confirm your subscription: {confirm_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, "A confirmation email has been sent. Please check your inbox.")
            else:
                messages.warning(request, "This email is already subscribed.")
            return redirect('home')
    else:
        form = NewsletterSignupForm()
    return render(request, 'newsletter/signup.html', {'form': form})

def newsletter_confirm(request, email_b64, token):
    try:
        email = force_str(urlsafe_base64_decode(email_b64))
        if signer.unsign(token) == email:
            subscriber = NewsletterSubscriber.objects.get(email=email)
            subscriber.confirmed = True
            subscriber.save()
            messages.success(request, "Your subscription has been confirmed!")
        else:
            messages.error(request, "Invalid confirmation token.")
    except (BadSignature, SignatureExpired):
        messages.error(request, "The confirmation link is invalid or has expired.")
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, "No subscription found for this email.")

    return redirect('home')