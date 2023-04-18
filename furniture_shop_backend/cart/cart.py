from furniture_shop import settings
from main.models import Product

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()

        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modifed = True

    def add(self, product: Product, count: int=1, update: bool=False):
        prod_pk = str(product.pk)
        old_count = self.cart.setdefault(prod_pk, dict()).get('count', '0')
        new_count = count if update else count + int(old_count)
        self.cart[prod_pk] = {
            'count': str(new_count),
            'price': str(product.price),
        }
        self.save()

    def delete(self, pk):
        prod_pk = str(pk)
        if prod_pk in self.cart:
            del self.cart[prod_pk]
            self.save()

    def clear(self):
        if self.session.get(settings.CART_SESSION_ID):
            del self.session[settings.CART_SESSION_ID]
            self.session.modifed = True
        self.cart = dict()

    def get_total_price(self):
        return sum(int(cart['count']) * int(cart['price']) for cart in self.cart.values())
    
    def __len__(self):
        return sum(int(cart['count']) for cart in self.cart.values())
    
    def __iter__(self):
        queryset = Product.objects.filter(id__in=self.cart.keys())
        for product in queryset:
            prod_pk = str(product.pk)
            count = int(self.cart[prod_pk]['count'])
            yield {
                'product': product,
                'count': count,
                'price': product.price,
                'total_price': product.price * count,
            }
