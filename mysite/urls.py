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
    path('', include('blog.urls')),
    path('products/', include('products.urls')),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", robots_txt, name="robots_txt")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
