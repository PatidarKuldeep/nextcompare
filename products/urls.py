from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),
    path('compare/', views.compare_products, name='compare_products'),
    path("search/", views.search, name="search"),
]