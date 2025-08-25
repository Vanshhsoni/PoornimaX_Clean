from django.urls import path
from . import views  # current app ke views
from accounts import views as account_views  # accounts app ke views

urlpatterns = [
    # Home page ko accounts ka login_signup bana do
    path('', account_views.login_signup, name='home'),
]
