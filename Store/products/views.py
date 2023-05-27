from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product, Product_category, Busket
from users.models import User
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    product = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(product, per_page)
    products_paginator = paginator.page(page_number)
    context = {
        'title': 'Store - Каталог',
        'categories': Product_category.objects.all(),
        'products': products_paginator,
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Busket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Busket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Busket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

