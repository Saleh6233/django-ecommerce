from itertools import product

from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.


def store(request):
    all_products = Product.objects.all()
    context = {'my_products': all_products}

    return render(request, 'store/store.html', context)


def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories': all_categories}


def list_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}

    return render(request, 'store/list-category.html', context)


def product_info(request, slug):

    product = get_object_or_404(Product, slug=slug)

    context = {'product': product,
               }

    return render(request, 'store/product-info.html', context)
