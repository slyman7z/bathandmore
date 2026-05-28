from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q



def store(request, category_slug=None):
    categories = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories,
            is_available=True
        ).order_by('id')
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        page_number = paginator.get_page(page)
        
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        page_number = paginator.get_page(page)
    

    product_count = products.count()
    

    context = {
        'products': page_number,
        'product_count': product_count,
    }

    return render(request, 'store.html', context)

def product_detail(request, category_slug, product_slug):
    color = request.GET.get('color')
    return HttpResponse(color)
    exit()

    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
        is_available=True
    )
    in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = product).exists()
    context = {
        'product': product,
        'in_cart': in_cart
    }

    return render(request, 'product_detail.html', context)


def search(request):
    keyword = request.GET.get('q', '')

    products = Product.objects.none()
    product_count = 0

    if keyword:
        products = Product.objects.filter(
           Q(product_name__icontains=keyword) | Q(description__icontains=keyword)   
        )

        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }

    return render(request, 'store.html', context)