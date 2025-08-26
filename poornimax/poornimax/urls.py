from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# 👇 sitemap imports
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap

# 👇 define sitemaps dict
sitemaps = {
    "static": StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('', include('poornima_site.urls')),
    path('accounts/', include('accounts.urls')),
    path('feed/', include('feed.urls')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),

    # Google verification file
    path(
        "google34a777b06ccf7e67.html",
        TemplateView.as_view(template_name="google34a777b06ccf7e67.html")
    ),

    # Sitemap
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # Robots.txt
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
