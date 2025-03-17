from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_form_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
]
