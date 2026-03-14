from django.db import models
from django.utils.text import slugify
from django.db.models import F
from products.utils.scoring import calculate_mobile_score, calculate_laptop_score
from django.urls import reverse
# Cloudinary
from cloudinary.models import CloudinaryField


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

    # Cloudinary Image
    image = CloudinaryField('image', blank=True, null=True)

    description = models.TextField(blank=True)

    affiliate_link = models.URLField(blank=True, null=True)
    
    MARKETPLACE_CHOICES = [
        ("amazon", "Amazon"),
        ("flipkart", "Flipkart"),
    ]
    marketplace = models.CharField(
        max_length=20,
        choices=MARKETPLACE_CHOICES,
        blank=True,
        null=True
    )

    overall_score = models.FloatField(default=0)
    performance_score = models.FloatField(default=0)
    camera_score = models.FloatField(default=0)
    manual_camera_score = models.FloatField(null=True, blank=True)
    battery_score = models.FloatField(default=0)

    verdict = models.CharField(max_length=100, blank=True)

    is_trending = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    # -------------------
    # Save Method
    # -------------------
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        self.overall_score = self.calculate_score()
        self.verdict = self.generate_verdict()

        super().save(*args, **kwargs)


    # -------------------
    # Score Calculation
    # -------------------
    def calculate_score(self):

        if hasattr(self, "mobilespecs"):

            from products.utils.scoring import calculate_mobile_scores

            scores = calculate_mobile_scores(self.mobilespecs)

            self.performance_score = scores["performance"]
            if self.manual_camera_score:
                self.camera_score = self.manual_camera_score
            else:
                self.camera_score = scores["camera"]

            self.battery_score = scores["battery"]

            ram_score = min((self.mobilespecs.ram / 16) * 100, 100)

            processor_score = (
                self.mobilespecs.processor.benchmark_score
                if self.mobilespecs.processor
                else 0
            )

            self.gaming_score = (processor_score * 0.7) + (ram_score * 0.3)

            overall = (
                self.performance_score * 0.45 +
                self.camera_score * 0.35 +
                self.battery_score * 0.20
            )
            return round(overall, 1)

        return 0


    # -------------------
    # Verdict Generator
    # -------------------
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
    camera = models.CharField(max_length=100)
    
    processor = models.ForeignKey(
        "Processor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    display_type = models.CharField(max_length=50)
    charging = models.CharField(max_length=50, blank=True, null=True)


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


# -------------------
# Processor Model
# -------------------
class Processor(models.Model):

    name = models.CharField(max_length=100)

    brand = models.CharField(max_length=50, blank=True)

    antutu_score = models.IntegerField(null=True, blank=True)

    geekbench_single = models.IntegerField(null=True, blank=True)

    geekbench_multi = models.IntegerField(null=True, blank=True)

    benchmark_score = models.IntegerField(default=0)


    def __str__(self):
        return self.name