from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

import weasyprint

from .models import OrderItem, Order
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


@method_decorator(staff_member_required, name='dispatch')
class OrderAdminDetailView(DetailView):
    template_name = 'admin/orders/order/detail.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request,
                      self.template_name,
                      {'order': order})


@method_decorator(staff_member_required, name='dispatch')
class OrderAdminPdfView(DetailView):
    template_name = 'orders/order/pdf.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        html = render_to_string(self.template_name, {'order': order})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(
                                                   settings.STATIC_ROOT + '/css/style.css')])
        return response
