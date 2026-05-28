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
    
 
# State and LGA models for shipping address form   
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    alias = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='lgas'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
