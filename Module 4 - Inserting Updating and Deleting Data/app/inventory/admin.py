from django.contrib import admin

from .models import (
    Category,
    Order,
    OrderProduct,
    Product,
    ProductPromotionEvent,
    PromotionEvent,
    StockManagement,
    User,
)


# Inline for Product Promotions in Product Admin
class ProductPromotionInline(admin.TabularInline):
    model = ProductPromotionEvent
    extra = 1


# Inline for Order Products in Order Admin
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "level")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


# Promotion Event Admin
@admin.register(PromotionEvent)
class PromotionEventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "price_reduction")
    search_fields = ("name",)


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_active",
        "is_digital",
        "created_at",
    )
    list_filter = ("is_active", "is_digital", "category")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductPromotionInline]


# Stock Management Admin
@admin.register(StockManagement)
class StockManagementAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "last_checked_at")
    search_fields = ("product__name",)


# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email")


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    list_filter = ("created_at",)
    inlines = [OrderProductInline]


# Order Product Admin
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")
    search_fields = ("order__id", "product__name")


# Register ProductPromotionEvent separately if needed
admin.site.register(ProductPromotionEvent)
