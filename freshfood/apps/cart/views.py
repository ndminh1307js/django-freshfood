from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from freshfood.apps.products.models import Product
from django.views.generic import View, DetailView

from .cart import Cart
from freshfood.apps.coupons.forms import CouponApplyForm
from freshfood.apps.products.recommender import Recommender


@method_decorator(require_POST, name='dispatch')
class CartAddView(View):
    """ Add a product to the cart """

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product,
                 quantity=1,
                 override_quantity=False)
        cart.save()
        # update checkout
        checkout = cart.get_checkout_info()
        return JsonResponse({'status': 'ok',
                             'checkout': checkout})


@method_decorator(require_POST, name='dispatch')
class CartRemoveView(View):
    """ Decrement by 1 a product quantity from the cart"""

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product=product)
        cart.save()
        # update checkout
        checkout = cart.get_checkout_info()
        return JsonResponse({'status': 'ok',
                             'checkout': checkout})


@method_decorator(require_POST, name='dispatch')
class CartClearItemView(View):
    """ Remove a product from the cart """

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.clearItem(product=product)
        cart.save()
        # update checkout
        checkout = cart.get_checkout_info()
        return JsonResponse({'status': 'ok',
                             'checkout': checkout})


class CartDetailView(DetailView):
    template_name = 'cart/detail.html'

    def get(self, request):
        cart = Cart(request)
        # update checkout
        checkout = cart.get_checkout_info()
        coupon_apply_form = CouponApplyForm()

        r = Recommender()
        cart_products = [item['product'] for item in cart]
        recommended_products = r.suggest_products_for(
            cart_products, max_results=4)

        return render(request,
                      self.template_name,
                      {'cart': cart,
                       'checkout': checkout,
                       'coupon_apply_form': coupon_apply_form,
                       'recommended_products': recommended_products})
