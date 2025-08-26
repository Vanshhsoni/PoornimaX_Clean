from django.urls import path
from . import views  # current app ccounts app ke views
app_name = "poornima_site"
urlpatterns = [
    # Home page ko accounts ka login_signup bana do
    path('', views.home, name='home'),
]
