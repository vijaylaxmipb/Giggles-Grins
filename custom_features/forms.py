from django import forms
from .models import ContactForm


class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message']

        
class CustomSignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        from allauth.account.forms import SignupForm  # ✅ local import to avoid circular import
        self.signup_form_class = SignupForm
        self.signup_form = self.signup_form_class(*args, **kwargs)

    def __getattr__(self, attr):
        # Redirect attribute access to the wrapped form
        return getattr(self.signup_form, attr)

    def save(self, request):
        return self.signup_form.save(request)
