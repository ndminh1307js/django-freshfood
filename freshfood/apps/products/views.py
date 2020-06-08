from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product
from .recommender import Recommender


class ProductListView(ListView):
    template_name = 'products/product/list.html'

    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()

        if category_slug:
            language = request.LANGUAGE_CODE
            category = get_object_or_404(Category,
                                         translations__language_code=language,
                                         translations__slug=category_slug)
            products = products.filter(category=category)

        return render(request,
                      self.template_name,
                      {'category': category,
                       'categories': categories,
                       'products': products})


class ProductDetailView(DetailView):
    template_name = 'products/product/detail.html'

    def get(self, request, id, slug):
        language = request.LANGUAGE_CODE
        product = get_object_or_404(Product,
                                    id=id,
                                    translations__language_code=language,
                                    translations__slug=slug)
        r = Recommender()
        recommended_products = r.suggest_products_for([product], 4)
        print(recommended_products)

        return render(request,
                      self.template_name,
                      {'product': product,
                       'recommend_products': recommended_products})
