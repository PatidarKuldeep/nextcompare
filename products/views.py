from django.shortcuts import render
from .models import Product
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Q



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
        category__name__icontains=category_name
    ).order_by("-created_at")


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

    return render(request, 'category.html', {
        "products": products,
        "category_name": category_name
    })

def compare_products(request):
    product_ids = request.GET.getlist('compare')

    products = Product.objects.filter(id__in=product_ids)

    context = {
        'products': products,
    }

    return render(request, 'compare.html', context)


def search(request):

    query = request.GET.get("q")

    results = []

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query)
        )

    context = {
        "query": query,
        "results": results
    }

    return render(request, "search.html", context)