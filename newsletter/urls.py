from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.newsletter_signup, name='newsletter_signup'),
    path('confirm/<str:email_b64>/<str:token>/', views.newsletter_confirm, name='newsletter_confirm'),
]
