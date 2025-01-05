from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories")
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(
        'Subcategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products")
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True)
    has_sizes = models.BooleanField(default=True)
    is_special_offer = models.BooleanField(
        default=False)  # Special offers flag

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed

    def __str__(self):
        return self.order_number