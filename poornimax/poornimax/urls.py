from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # 👈 add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('poornima_site.urls')),
    path('accounts/', include('accounts.urls')), 
    path('feed/', include('feed.urls')),
    path('chat/', include('chat.urls', namespace='chat')),

    # 👇 Google verification file (replace filename with your actual one)
    path(
        "google123456789abc.html",  
        TemplateView.as_view(template_name="google123456789abc.html")
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
