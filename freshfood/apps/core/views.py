from django.shortcuts import render
from django.views.generic import View

from freshfood.apps.products.models import Category, Product


class HomepageView(View):
    template_name = 'home/index.html'

    def get(self, request):
        new_products = Product.objects.all()[:6]
        categories = Category.objects.all()

        return render(request,
                      self.template_name,
                      {'new_products': new_products,
                       'categories': categories})
