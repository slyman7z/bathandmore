from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
    
    
    cart_item, created = CartItem.objects.get_or_create(
        product=product, 
        cart=cart,
        defaults={'quantity': 1, 'is_active': True}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.is_active = True 
        cart_item.save()
    
    next_url = request.GET.get('next')
    return redirect(next_url or 'cart')  

def remove_cart_item(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # Keep filter specific to active items if that matches your business logic
        cart_item = CartItem.objects.filter(product_id=product_id, cart=cart).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        CartItem.objects.filter(product_id=product_id, cart=cart).delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart')
    
def cart(request):
    # Define local tracking variables cleanly inside the function scope
    total = Decimal('0.00')
    quantity = 0
    cart_items = None
    tax = Decimal('0.00')
    grand_total = Decimal('0.00')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        
        # select_related('product') fetches the product details alongside the cart item in ONE query
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).select_related('product')

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (total * Decimal('0.075')).quantize(Decimal('0.01'))
        grand_total = (total + tax).quantize(Decimal('0.01'))

    except Cart.DoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, 'cart.html', context)