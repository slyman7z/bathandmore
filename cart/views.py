from django.shortcuts import render, redirect, get_object_or_404
from store . models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal, ROUND_HALF_UP

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))   
    try:    
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
    
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')   

def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
    

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()

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
    product = get_object_or_404(Product, id=product_id)
    



def cart(request, total=Decimal('0.00'), quantity=0, cart_items=None):

    tax = Decimal('0.00')
    grand_total = Decimal('0.00')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

        cart_items = CartItem.objects.filter(
            cart=cart,
            is_active=True
        )

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = total * Decimal('0.075')
        grand_total = total + tax

        # rounding (final step)
        tax = tax.quantize(Decimal('0.01'))
        grand_total = grand_total.quantize(Decimal('0.01'))

    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, 'cart.html', context)