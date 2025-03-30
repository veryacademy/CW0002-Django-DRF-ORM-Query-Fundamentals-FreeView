from inventory.models import (
    Category,
    Order,
    OrderProduct,
    Product,
    StockManagement,
    User,
)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "parent", "name", "slug", "is_active", "level"]


class CategoryReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class StockManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManagement
        fields = ["quantity"]


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_digital",
            "is_active",
            "price",
            "category",
        ]


class CreateProductStockSerializer(serializers.ModelSerializer):
    stock_data = StockManagementSerializer(write_only=True, required=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_digital",
            "is_active",
            "price",
            "category",
            "stock_data",
        ]

    def create(self, validated_data):
        stock_data = validated_data.pop("stock_data", None)
        product = Product.objects.create(**validated_data)
        StockManagement.objects.create(product=product, **stock_data)

        return product

    def to_representation(self, instance):
        """Customize the representation to include stock data."""
        # Start with the default representation
        data = super().to_representation(instance)

        # Fetch the related stock data from the StockManagement model
        stock_instance = StockManagement.objects.filter(product=instance).first()

        # If stock data exists, add it to the response
        if stock_instance:
            data["stock_data"] = StockManagementSerializer(stock_instance).data
        else:
            data["stock_data"] = None  # In case there's no related stock data

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    """Handles individual product entries within an order"""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """Handles order creation with multiple products"""

    products = OrderProductSerializer(
        many=True, write_only=True
    )  # Accept a list of products

    class Meta:
        model = Order
        fields = ["user", "created_at", "updated_at", "products"]

    def create(self, validated_data):
        products_data = validated_data.pop("products")  # Extract product list
        order = Order.objects.create(**validated_data)  # Create the order

        # Create OrderProduct entries for each product in the request
        order_products = [
            OrderProduct(order=order, **product_data) for product_data in products_data
        ]
        OrderProduct.objects.bulk_create(order_products)  # Bulk insert

        return order


class CategoryBulkDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of category IDs to delete",
    )


# class CreateProductSerializer(serializers.ModelSerializer):
#     new_category = serializers.SerializerMethodField()
#     stock = StockManagementSerializer(write_only=True, required=True)

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "description",
#             "is_digital",
#             "is_active",
#             "price",
#             "new_category",  # Accepts full category data
#             "stock",
#         ]

#     def get_new_category(self, obj):
#         """Returns the category info when reading the object"""
#         return CategorySerializer(obj.category).data if obj.category else None

#     def to_internal_value(self, data):
#         """
#         Override to_internal_value to handle category manually before DRF tries to validate it.
#         """
#         category_data = data.pop("new_category", None)
#         validated_data = super().to_internal_value(data)

#         if category_data:
#             category_obj, _ = Category.objects.get_or_create(
#                 name=category_data["name"],
#                 defaults={
#                     "slug": category_data.get("slug", ""),
#                     "is_active": category_data.get("is_active", True),
#                     "level": category_data.get("level", 1),
#                     "parent": category_data.get("parent", None),
#                 },
#             )
#             validated_data["category"] = category_obj

#         return validated_data

#     def create(self, validated_data):
#         """
#         This method now receives an already validated category instance,
#         so it won't trigger a duplicate insert.
#         """
#         stock_data = validated_data.pop("stock", None)

#         # Create the product
#         product = Product.objects.create(**validated_data)

#         # Create stock entry
#         StockManagement.objects.create(product=product, **stock_data)

#         return product
