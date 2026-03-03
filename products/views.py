from django.shortcuts import render
from .models import Product
from datetime import date, timedelta
from django.shortcuts import get_object_or_404



def home(request):
    recent_date = date.today() - timedelta(days=30)

    recent_products = Product.objects.filter(
        launch_date__gte=recent_date
    ).order_by('-launch_date')[:6]

    best_products = Product.objects.order_by('-overall_score')[:6]

    context = {
        'recent_products': recent_products,
        'best_products': best_products,
    }

    return render(request, 'home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product,
    }

    return render(request, 'product_detail.html', context)

def category_view(request, category_name):
    products = Product.objects.filter(
        category__name__iexact=category_name
    )

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    products = products.order_by('-overall_score')

    context = {
        'products': products,
        'category_name': category_name,
    }

    return render(request, 'category.html', context)

def compare_products(request):
    product_ids = request.GET.getlist('compare')

    products = Product.objects.filter(id__in=product_ids)

    context = {
        'products': products,
    }

    return render(request, 'compare.html', context)