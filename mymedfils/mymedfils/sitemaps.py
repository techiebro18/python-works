from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['ecommerce:home', "ecommerce:page kwargs={'slug':'about-us'}"]

    def location(self, item):
        return reverse(item)


        