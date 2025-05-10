from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_form_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('contact/success/', views.contact_success, name='contact_success'),
]
