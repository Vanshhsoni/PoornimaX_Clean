# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # yahan apne url "name" dalne hain (app_name:url_name format)
        return [
            "poornima_site:home",     # 👈 root landing page (/)
            # agar aur chahiye to add here
            # "accounts:login_signup",
            # "accounts:load_login",
        ]

    def location(self, item):
        return reverse(item)
