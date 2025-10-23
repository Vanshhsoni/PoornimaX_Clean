from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup_or_login/', views.load_signup, name='load_signup'),
    path('signup/', views.login_signup, name='login_signup'),
    path('signup_access/', views.signup_access, name='signup_access'),
    path('login/', views.load_login, name='load_login'),
    path('login_access/', views.login_access, name='login_access'),
    
    # path('verify-otp/', views.verify_otp, name='verify_otp'),  # ❌ OTP disabled

    path('logout/', views.logout_view, name='logout'),
    path('questionnaire/', views.questionnaire_view, name='questionnaire_view'),
    path('ans/', views.answers_view, name='answers_page'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('x/', views.x, name='x'),
    path('z/', views.z, name='z'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
