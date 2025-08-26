# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # yahan apne url "name" dalne hain (not paths)
        return [
            "feed:home",              # accounts.urls → signup page

        ]

    def location(self, item):
        return reverse(item)
