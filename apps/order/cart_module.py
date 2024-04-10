from django.contrib import messages

from apps.product.models import BoardGame

CART_SESSION_ID = 'cart'
PRODUCT = BoardGame


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.total_before_discount = 0
        self.total_discount = 0
        self.total_after_discount = 0
        self.post_price = 70000

        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item["product"] = PRODUCT.objects.get(pk=int(item['id']))
            if item["discounted_price"]:
                item['total'] = item['quantity'] * item['discounted_price']
            else:
                item['total'] = item['quantity'] * item['original_price']
            yield item

    def remove_cart(self):
        cart = self.session[CART_SESSION_ID] = {}

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'original_price': product.price,
                'discounted_price': product.discounted_price() if product.discount > 0 else None,
                'id': product_id
            }

        total_quantity = int(quantity) + self.cart[product_id]['quantity']
        if total_quantity > product.stock:
            messages.error(self.request,
                           f"متاسفانه موجودی این محصول کمتر از مقدار درخواستی شماست. (موجودی فعلی: {product.stock})")
            return False

        self.cart[product_id]['quantity'] += int(quantity)
        self.save()
        return True

    def delete(self, product_id):
        del self.cart[str(product_id)]
        self.save()

    def get_totals(self):
        cart_items = self.cart.values()

        for item in cart_items:
            self.total_before_discount += item['quantity'] * item['original_price']
            if item['discounted_price']:
                self.total_discount += item['quantity'] * (item['original_price'] - item['discounted_price'])

        self.total_after_discount = self.post_price + self.total_before_discount - self.total_discount

    def save(self):
        self.session.modified = True
