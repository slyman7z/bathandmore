from django.db.models import Sum
from cart.models import Cart, CartItem 
from cart.views import _cart_id

def cart_count(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        result = CartItem.objects.filter(cart=cart).aggregate(total_qty=Sum('quantity'))
        cart_count = result['total_qty'] or 0
    except Cart.DoesNotExist:
        cart_count = 0

    return {'cart_count': cart_count}