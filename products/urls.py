from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),
    path('compare/', views.compare_products, name='compare_products'),
    path("search/", views.search, name="search"),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
    path(
        "best/<str:category_name>/<int:price>/",
        views.best_products,
        name="best_products"),
    path(
        "compare/<slug:slug1>-vs-<slug:slug2>/",
        views.compare_slug,
        name="compare_slug"),
    path(
        "popular-comparisons/",
        views.popular_comparisons,
        name="popular_comparisons"),
    path(
        "brand/<slug:brand_name>/",
        views.brand_page,
        name="brand_page"),
    path(
        "top-<str:category>/",
        views.top_products,
        name="top_products"),
        path("processors/", views.processor_ranking, name="processor_ranking"),
]