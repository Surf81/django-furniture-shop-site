from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from main.models import Product
from .cart import Cart


def cart_view(request):
    return render(request, 'cart/cart.html')


def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)

    cart.add(product)
    if (path := request.META.get('HTTP_REFERER')):
        return redirect(path)
    else:
        return redirect('cart:cart_view')


def cart_sub(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)

    cart.add(product, -1)
    if (path := request.META.get('HTTP_REFERER')):
        return redirect(path)
    else:
        return redirect('cart:cart_view')


def cart_del(request, pk):
    cart = Cart(request)
    cart.delete(pk)
    if (path := request.META.get('HTTP_REFERER')):
        return redirect(path)
    else:
        return redirect('cart:cart_view')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    if (path := request.META.get('HTTP_REFERER')):
        return redirect(path)
    else:
        return redirect('cart:cart_view')
