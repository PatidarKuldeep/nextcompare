from django.db import models
from django.utils.text import slugify
from django.db.models import F


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
        score = 0

        if self.category.name.lower() == "mobile" and hasattr(self, "mobilespecs"):
            spec = self.mobilespecs

            if spec.ram >= 8:
                score += 20
            elif spec.ram >= 6:
                score += 15

            if spec.battery >= 5000:
                score += 20

            if spec.processor_score >= 800:
                score += 25

            if spec.camera >= 64:
                score += 20

            if spec.display_type.lower() == "amoled":
                score += 15

        elif self.category.name.lower() == "laptop" and hasattr(self, "laptopspecs"):
            spec = self.laptopspecs

            if spec.ram >= 16:
                score += 25
            elif spec.ram >= 8:
                score += 20

            if spec.processor_score >= 1000:
                score += 30

            if spec.storage >= 512:
                score += 15

            if spec.gpu:
                score += 20

            if spec.battery_backup >= 6:
                score += 10

        return score

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
    processor_score = models.IntegerField()
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
    processor_score = models.IntegerField()
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