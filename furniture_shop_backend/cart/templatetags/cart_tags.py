from django import template

register = template.Library()

@register.inclusion_tag('cart/.inc/cart_widget.html')
def cart_widget(label, cart, href="", cls="", empty_cls=""):
    if not empty_cls:
        empty_cls = "empty_cart"

    options = {
        'count': len(cart),
        'total': cart.get_total_price(),
        'class': cls,
        'class_empty': empty_cls if not len(cart) else "",
        'href': href,
        'label': label,
    }
    return {'cart': options}