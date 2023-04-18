from .cart import Cart

def furniture_shop_context_processor(request):
    context = {}
    context['cart'] = Cart(request)
    return context