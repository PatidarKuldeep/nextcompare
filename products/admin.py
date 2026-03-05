from django.contrib import admin
from .models import Category, Brand, Product, MobileSpecs, LaptopSpecs


class MobileSpecsInline(admin.StackedInline):
    model = MobileSpecs
    extra = 0


class LaptopSpecsInline(admin.StackedInline):
    model = LaptopSpecs
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "overall_score", "verdict", "is_trending")
    prepopulated_fields = {"slug": ("name",)}

    def get_inlines(self, request, obj=None):
        if obj:
            if "mobile" in obj.category.name.lower():
                return [MobileSpecsInline]
            elif "laptop" in obj.category.name.lower():
                return [LaptopSpecsInline]
        return []

admin.site.register(Category)
admin.site.register(Brand)