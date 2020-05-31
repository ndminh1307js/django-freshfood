from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import OrderItem
from .forms import OrderCreateForm
from freshfood.apps.cart.cart import Cart

from .tasks import order_created


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
            # launch asynchronous task
            order_created.delay(order.id)
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})

            # set the order id in the section
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    def get(self, request):
        cart = Cart(request)
        checkout = cart.get_checkout_info()
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart,
                       'checkout': checkout,
                       'form': form})
