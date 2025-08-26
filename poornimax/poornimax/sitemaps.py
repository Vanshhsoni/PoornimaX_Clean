# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # yahan apne url "name" dalne hain (not paths)
        return [
            "home",            # poornima_site.urls → home view
            "login_signup",    # accounts.urls → signup page
            "load_login",      # accounts.urls → login page
        ]

    def location(self, item):
        return reverse(item)
