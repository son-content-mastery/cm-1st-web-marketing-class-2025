from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import robots_txt

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, PostSitemap, CategorySitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('products.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", robots_txt, name="robots_txt")
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

