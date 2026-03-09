from django.db import models
from django.utils.text import slugify
from django.db.models import F
from products.utils.scoring import calculate_mobile_score, calculate_laptop_score


# -------------------
# Category Model
# -------------------
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# -------------------
# Brand Model
# -------------------
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -------------------
# Product Model
# -------------------
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    price = models.IntegerField()
    launch_date = models.DateField()

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)

    affiliate_link = models.URLField(blank=True, null=True)

    overall_score = models.FloatField(default=0)
    verdict = models.CharField(max_length=100, blank=True)

    is_trending = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.overall_score = self.calculate_score()
        self.verdict = self.generate_verdict()

        super().save(*args, **kwargs)
        
    def calculate_score(self):
        if hasattr(self, "mobilespecs"):
            return calculate_mobile_score(self.mobilespecs)
        if hasattr(self, "laptopspecs"):
            return calculate_laptop_score(self.laptopspecs)
        return 0

    def generate_verdict(self):
        if self.overall_score >= 85:
            return "Best Overall"
        elif self.overall_score >= 70:
            return "Excellent Choice"
        elif self.overall_score >= 60:
            return "Good Option"
        else:
            return "Average"

    def __str__(self):
        return self.name


# -------------------
# Mobile Specs
# -------------------
class MobileSpecs(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    ram = models.IntegerField()
    storage = models.IntegerField()
    battery = models.IntegerField()
    camera = models.IntegerField()
    processor = models.ForeignKey(
        "Processor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    display_type = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        score = product.calculate_score()
        verdict = product.generate_verdict()
        Product.objects.filter(id=product.id).update(
            overall_score=score,
            verdict=verdict
            )
    def __str__(self):
        return f"Specs for {self.product.name}"
# -------------------
# Laptop Specs
# -------------------
class LaptopSpecs(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    ram = models.IntegerField()
    storage = models.IntegerField()
    processor = models.ForeignKey(
        "Processor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    gpu = models.BooleanField(default=False)
    battery_backup = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        score = product.calculate_score()
        verdict = product.generate_verdict()
        Product.objects.filter(id=product.id).update(
            overall_score=score,
            verdict=verdict
            )

    def __str__(self):
        return f"Specs for {self.product.name}"


class Processor(models.Model):

    name = models.CharField(max_length=100)

    brand = models.CharField(max_length=50, blank=True)

    antutu_score = models.IntegerField(null=True, blank=True)

    geekbench_single = models.IntegerField(null=True, blank=True)

    geekbench_multi = models.IntegerField(null=True, blank=True)

    benchmark_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name