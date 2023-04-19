from furniture_shop import settings
from main.models import Product, UserProductRelated
import collections

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.session_use = True

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()

        self.cart = cart

        if request.user.is_authenticated:
            self.session_use = False
            self.save(self.load_cart())
            del self.session[settings.CART_SESSION_ID]
            self.session.modifed = True

    def save(self, prod):
        def productrelated_save(prod_pk):
            if not(product := self.cart[prod_pk].get('product')):
                product = Product.objects.get(pk=prod_pk)
            productrelated, _ = UserProductRelated.objects.get_or_create(product=product, user=self.request.user)
            productrelated.count_on_cart = int(self.cart.get(prod_pk, dict()).get('count', 0))
            productrelated.save()

        if self.session_use:
            self.session[settings.CART_SESSION_ID] = self.cart
            self.session.modifed = True
        else:
            if hasattr(prod, '__iter__'):
                for prod_pk in prod:
                    productrelated_save(prod_pk)
            else:
                productrelated_save(prod)

    def add(self, product: Product, count: int=1, update: bool=False, need_save: bool=True):
        prod_pk = str(product.pk)
        old_count = self.cart.setdefault(prod_pk, dict()).get('count', '0')
        new_count = count if update else count + int(old_count)
        self.cart[prod_pk] = {
            'count': str(new_count),
            'price': str(product.price),
        }
        if not self.session_use:
            self.cart[prod_pk]['product'] = product

        if need_save:
            self.save(prod_pk)

    def load_cart(self):
        old_cart = set(self.cart)
        productsrelated = UserProductRelated.objects.filter(user=self.request.user.pk, count_on_cart__gt=0).select_related('product')
        for prod in productsrelated:
            if (prod_pk := str(prod.product.pk)) not in self.cart:
                self.add(prod.product, count=prod.count_on_cart, need_save=False)
                old_cart.discard(prod_pk)
        return old_cart

    def delete(self, pk):
        prod_pk = str(pk)
        if prod_pk in self.cart:
            del self.cart[prod_pk]
            self.save(prod_pk)

    def clear(self):
        prod_pk_to_clear = [prod_pk for prod_pk in self.cart.keys()]
        self.cart = dict()
        self.save(prod_pk_to_clear)
        if self.session.get(settings.CART_SESSION_ID):
            del self.session[settings.CART_SESSION_ID]
            self.session.modifed = True

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
