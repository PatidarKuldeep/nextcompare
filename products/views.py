from django.shortcuts import render, get_object_or_404
from .models import Product
from datetime import date, timedelta
from django.db.models import Q
from django.http import JsonResponse


def home(request):

    recent_date = date.today() - timedelta(days=30)

    recent_products = Product.objects.filter(
        launch_date__gte=recent_date
    ).order_by('-launch_date')[:6]

    best_products = Product.objects.order_by('-overall_score')[:6]

    trending_products = Product.objects.filter(
        is_trending=True
    ).order_by('-overall_score')[:6]

    context = {
        'recent_products': recent_products,
        'best_products': best_products,
        'trending_products': trending_products,
    }

    return render(request, 'home.html', context)


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)

    # Similar products
    similar_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).order_by("-overall_score")[:4]

    # Products for compare dropdown
    compare_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:20]

    # Smart compare suggestions (top scoring)
    compare_suggestions = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).order_by("-overall_score")[:3]

    context = {
        "product": product,
        "similar_products": similar_products,
        "compare_products": compare_products,
        "compare_suggestions": compare_suggestions,
    }

    return render(request, "product_detail.html", context)

def category_view(request, category_name):

    products = Product.objects.filter(category__name__iexact=category_name)

    # Common Filters
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # Mobile Filters
    ram = request.GET.get("ram")
    storage = request.GET.get("storage")
    battery = request.GET.get("battery")

    if category_name.lower() == "mobiles":

        if ram:
            try:
                products = products.filter(mobilespecs__ram=int(ram))
            except:
                pass

        if storage:
            try:
                products = products.filter(mobilespecs__storage=int(storage))
            except:
                pass

        if battery:
            try:
                products = products.filter(mobilespecs__battery__gte=int(battery))
            except:
                pass

    # Laptop Filters
    if category_name.lower() == "laptops":

        if ram:
            try:
                products = products.filter(laptopspecs__ram=int(ram))
            except:
                pass

        if storage:
            try:
                products = products.filter(laptopspecs__storage=int(storage))
            except:
                pass

    context = {
        "products": products,
        "category_name": category_name
    }

    return render(request, "category.html", context)


def compare_products(request):

    product_ids = request.GET.getlist("compare")

    products = Product.objects.filter(id__in=product_ids)

    if len(products) < 2:
        return render(request, "compare.html", {
            "error": "Please select at least 2 products to compare."
        })

    context = {
        "products": products
    }

    return render(request, "compare.html", context)

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


def search_suggestions(request):

    query = request.GET.get("q", "")

    results = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query)
        )[:5]

        for p in products:
            results.append({
                "name": p.name,
                "slug": p.slug
            })

    return JsonResponse({"results": results})

def best_products(request, category_name, price):

    products = Product.objects.filter(
        category__name__iexact=category_name,
        price__lte=price
    ).order_by("-overall_score")[:10]

    context = {
        "products": products,
        "category_name": category_name,
        "price": price
    }

    return render(request, "best_products.html", context)

def compare_slug(request, slug1, slug2):

    p1 = get_object_or_404(Product, slug=slug1)
    p2 = get_object_or_404(Product, slug=slug2)

    products = [p1, p2]

    context = {
        "products": products
    }

    return render(request, "compare.html", context)

def popular_comparisons(request):

    products = Product.objects.order_by("-overall_score")[:10]

    comparisons = []

    for i in range(len(products)):
        for j in range(i+1, len(products)):

            p1 = products[i]
            p2 = products[j]

            comparisons.append({
                "p1": p1,
                "p2": p2
            })

            if len(comparisons) >= 10:
                break

        if len(comparisons) >= 10:
            break

    context = {
        "comparisons": comparisons
    }

    return render(request, "popular_comparisons.html", context)

def brand_page(request, brand_name):

    brand_products = Product.objects.filter(
        brand__name__iexact=brand_name
    ).order_by("-overall_score")

    context = {
        "brand_name": brand_name,
        "products": brand_products
    }

    return render(request, "brand_page.html", context)