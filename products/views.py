from django.shortcuts import render, get_object_or_404
from .models import Product, Category, FAQ


def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True).exclude(id=product.id)[:4] 
    context = {
        'product': product, 
        'related_products': related_products
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True)
    faqs = category.faqs.all()  # Get all FAQs for this category

    context = {
        'category': category,
        'products': products,
        'faqs': faqs
    }
    return render(request, 'products/category_detail.html', context)


from django.http import HttpResponse
from django.conf import settings

def robots_txt(request):
    # Dynamically generate the robots.txt content
    lines = [
        "User-agent: *",
        "Disallow: /admin/",  # Disallow access to the admin panel
        "Disallow: /private/",  # Disallow access to private pages (if any)
        "",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",  # Reference to your sitemap
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
