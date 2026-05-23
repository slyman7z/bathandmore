from django.db import models
from category.models import Category
from django.urls import reverse


# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='photos/products', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    def get_url(self):
        return reverse( 'product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
