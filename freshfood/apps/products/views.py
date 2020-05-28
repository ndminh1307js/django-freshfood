from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product


class ProductListView(ListView):
    template_name = 'products/product/list.html'

    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        return render(request,
                      self.template_name,
                      {'category': category,
                       'categories': categories,
                       'products': products})


class ProductDetailView(DetailView):
    template_name = 'products/product/detail.html'

    def get(self, request, id, slug):
        product = get_object_or_404(Product,
                                    id=id,
                                    slug=slug)

        return render(request,
                      self.template_name,
                      {'product': product})
