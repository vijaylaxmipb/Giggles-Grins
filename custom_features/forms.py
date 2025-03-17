from django import forms
from .models import ContactForm


try:
    from allauth.account.forms import SignupForm
except ImportError:
    SignupForm = None


class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message']


class CustomSignupForm(SignupForm if SignupForm else forms.Form):  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def save(self, request):
        user = super().save(request)
        return user
