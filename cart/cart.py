from decimal import Decimal
from store.models import Product


class Cart():

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        # New user - generate a new session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        else:
            self.cart[product_id] = {'price': str(product.price),
                                     'qty': product_qty}

        self.session.modified = True

    def __len__(self):

        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):

        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])

            item['total'] = item['price'] * item['qty']

            yield item

    def get_total(self):

        total = 0  # Initialize total to 0

        # Iterate over each item in the cart
        for item in self.cart.values():
            # Convert price to Decimal and multiply by quantity to get the item's total price
            item_total = Decimal(item['price']) * item['qty']

            # Add the item total to the running total
            total += item_total

        return total  # Return the final total
