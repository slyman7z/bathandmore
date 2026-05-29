from django.db import models
from category.models import Category
from django.urls import reverse


# ================= PRODUCT =================

class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    product_image = models.ImageField(
        upload_to='photos/products',
        blank=True
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse(
            'product_detail',
            args=[self.category.slug, self.slug]
        )

    def __str__(self):
        return self.product_name


# # ================= VARIATION MANAGER =================

# class VariationManager(models.Manager):

#     def colors(self):
#         return self.filter(
#             variation_category='color',
#             is_active=True
#         )

#     def sizes(self):
#         return self.filter(
#             variation_category='size',
#             is_active=True
#         )


# # ================= VARIATION =================

# variation_category_choice = (
#     ('color', 'Color'),
#     ('size', 'Size'),
# )


# class Variation(models.Model):

#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='variations'
#     )

#     variation_category = models.CharField(
#         max_length=100,
#         choices=variation_category_choice
#     )

#     variation_value = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)

#     created_date = models.DateTimeField(auto_now_add=True)

#     # Managers
#     objects = models.Manager()
#     variation_set = VariationManager()

#     def __str__(self):
#         return self.variation_value


# # ================= STATE =================

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    alias = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# ================= LGA =================

class LGA(models.Model):

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='lgas'
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ================= PERSON =================

class Person(models.Model):

    name = models.CharField(max_length=100)

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE
    )

    lga = models.ForeignKey(
        LGA,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name