from decimal import Decimal
from django.conf import settings

from freshfood.apps.products.models import Product
from freshfood.apps.coupons.models import Coupon


class Cart(object):
    """ Initialize the cart """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = request.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity if it existed
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # mark the session asa 'modified' to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Decrement the quantity of a product by 1
        """
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] == 0:
                self.clearItem(product)

        self.save()

    def clearItem(self, product):
        """Remove a product from the cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the product
        from the database
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Get total price
        """
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )

    def get_total_quantity(self):
        """Get total item quantity in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_checkout_info(self):
        """Get all values for checkout process"""
        # get checkout information
        cart_total = self.get_total_price()
        delivery = 5
        # get total items quantity
        total_quantity = self.get_total_quantity()
        return {
            'total_quantity': total_quantity,
            'cart_total': cart_total,
            'delivery': delivery,
        }

    def clear(self):
        """ Clear all items in the cart """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return (self.get_total_price() - self.get_discount()) + self.get_checkout_info()['delivery']
