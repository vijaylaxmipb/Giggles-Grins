from django import forms
from .models import ContactForm
from allauth.account.forms import SignupForm as AllauthSignupForm, LoginForm as AllauthLoginForm


# Contact Form ModelForm
class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message']


# Custom Signup Form extending allauth's SignupForm
class CustomSignupForm(AllauthSignupForm):
    full_name = forms.CharField(max_length=100, label='Full Name', required=True)

    def save(self, request):
        user = super().save(request)
        full_name = self.cleaned_data.get('full_name')
        if full_name:
            parts = full_name.strip().split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
            user.save()
        return user


# Custom Login Form extending allauth's LoginForm
class CustomLoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(['login', 'password'])
