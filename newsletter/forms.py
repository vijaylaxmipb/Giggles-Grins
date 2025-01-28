
from django import forms

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(
        label='Enter your email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address',
            'class': 'form-control',
        }),
    )
