from django.shortcuts import render, get_object_or_404
from .models import Product, Category, FAQ


def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, category_slug, product_slug):
    # Get the category and ensure the product belongs to it
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category, available=True)

    # Query related products (same category, exclude current product)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    context = {
        'category': category,
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    # Get the category
    category = get_object_or_404(Category, slug=slug)

    # Get products and FAQs for the category
    products = category.products.filter(available=True)
    faqs = category.faqs.all()

    # Get related blog posts for the category
    related_posts = category.related_posts.all()[:3]

    context = {
        'category': category,
        'products': products,
        'faqs': faqs,
        'related_posts': related_posts, 
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
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",  # อ้างอิงไปที่ sitemap ของเรา
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
