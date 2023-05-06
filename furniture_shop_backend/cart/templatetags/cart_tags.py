from django import template

register = template.Library()

@register.inclusion_tag('cart/.inc/cart_widget.html')
def cart_widget(cart, href="", cls=""):
    options = {
        'count': len(cart),
        'total': cart.get_total_price(),
        'class': cls,
        'href': href,
    }
    return {'cart': options}