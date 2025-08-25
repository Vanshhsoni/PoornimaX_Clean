from django.urls import path
from . import views  # current app ccounts app ke views

urlpatterns = [
    # Home page ko accounts ka login_signup bana do
    path('', views.home, name='home'),
]
