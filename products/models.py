from django.db import models
from django.urls import reverse
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    related_posts = models.ManyToManyField(
        'blog.Post',  # Reference to the Post model in the blog app
        blank=True,
        related_name='categories',  # Allows accessing categories from a Post object
        null=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    body = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Affiliate Links
    shopee_affiliate_link = models.URLField(blank=True, null=True, help_text="Affiliate link for Shopee")
    lazada_affiliate_link = models.URLField(blank=True, null=True, help_text="Affiliate link for Lazada")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Include both category_slug and product_slug
        return reverse('product_detail', kwargs={
            'category_slug': self.category.slug,
            'product_slug': self.slug
        })
    

class FAQ(models.Model):
    category = models.ForeignKey(Category, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'