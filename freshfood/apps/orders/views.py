from django.shortcuts import render
from django.views.generic import CreateView

from .models import OrderItem
from .forms import OrderCreateForm
from freshfood.apps.cart.cart import Cart


class OrderCreateView(CreateView):
    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # clear the cart
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})

    def get(self, request):
        cart = Cart(request)
        checkout = cart.get_checkout_info()
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart,
                       'checkout': checkout,
                       'form': form})
