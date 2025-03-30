from django.db import models


# Category Model
class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.RESTRICT, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    is_active = models.BooleanField(default=False)
    level = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


# Promotion Event Model
class PromotionEvent(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price_reduction = models.IntegerField()

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    description = models.TextField(null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# Product Promotion Event Model
class ProductPromotionEvent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promotion_event = models.ForeignKey(PromotionEvent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("product", "promotion_event")

    def __str__(self):
        return f"{self.product.name} - {self.promotion_event.name}"


# Stock Management Model
class StockManagement(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True)
    quantity = models.IntegerField(default=0)
    last_checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock for {self.product.name}"


# User Model (can extend from AbstractBaseUser for custom user)
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=60)

    def __str__(self):
        return self.username


# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# Order Product Model
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ("product", "order")

    def __str__(self):
        return f"Product {self.product.name} in Order {self.order.id}"
