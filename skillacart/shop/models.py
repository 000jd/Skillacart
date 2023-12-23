from io import BytesIO
import random
import string
from PIL import Image
from django.db import models
from accounts.models import Users
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files import File

from djrichtextfield.models import RichTextField


class ProductCategory(models.Model):
    # Fields from products_productcategory entity
    name = models.CharField(max_length=100, db_index=True) 
    icon = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True, db_index=True) 
    created_at = models.DateTimeField(auto_now_add=True, db_index=True) 
    updated_at = models.DateTimeField(auto_now=True, db_index=True)  

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't exist
            self.slug = unique_slug_generator(self)  # Generate unique slug
        super(ProductCategory, self).save(*args, **kwargs)


class Product(models.Model):
    # Fields from products_product entity
    added_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='added_products',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200, db_index=True)  # Add db_index for name
    slug = models.SlugField(unique=True, null=True, blank=True, db_index=True)  # Add db_index for slug
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = RichTextField()
    images = models.ManyToManyField('ProductImage', blank=True, related_name='product_images')
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')

    class Meta:
        indexes = [
            models.Index(fields=['name', 'slug']),  
            models.Index(fields=['created_at']),    
        ]

    def __str__(self):
        return self.name

    def get_admin_user(self):
        admin_users = Users.objects.filter(is_admin=True)
        return admin_users.first() if admin_users.exists() else None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        if not self.added_by_id:
            self.added_by = self.get_admin_user()
        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    # Fields for the Image model
    image = models.ImageField(upload_to='uploads/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', db_index=True)  
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='product_reviews', db_index=True)  
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], db_index=True) 
    review_text = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    
def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)  # Use the instance's name for slug generation

    qs = instance.__class__.objects.filter(slug=slug)
    if qs.exists():
        new_slug = f"{slug}-{random_string_generator()}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug