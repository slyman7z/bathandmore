from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField( max_length=50, unique=True)
    description = models.TextField()
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name
    
    
