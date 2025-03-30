from drf_spectacular.utils import (
    extend_schema,
)
from inventory.models import Category
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    CategoryBulkDeleteSerializer,
    CategoryReturnSerializer,
    CategorySerializer,
    CreateProductSerializer,
    CreateProductStockSerializer,
    OrderSerializer,
    UserSerializer,
)

# class InventoryCategoryModelViewSet(ModelViewSet):
#     queryset = Category.objects.all()  # Fetch all categories
#     serializer_class = InventoryCategorySerializer  # Use the serializer

# class InventoryCategoryViewSet(ViewSet):
#     def list(self, request):
#         queryset = Category.objects.all()
#         serializer = InventoryCategorySerializer(queryset, many=True)
#         return Response(serializer.data)

####
#  Ex.1 Inserting Data with create() and save=()
####


class CategoryInsertViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer,  # This links the serializer for the request body
        responses={
            201: CategoryReturnSerializer
        },  # Expected response will be the created category
        tags=["Module 4"],
    )
    def create(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category_instance = serializer.save()

            return_serializer = CategoryReturnSerializer(category_instance)

            return Response(return_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


####
#  Ex.2 Bulk Insert with bulk_create()
####


class CategoryBulkInsertViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer(many=True),  # Accepts multiple objects
        responses={
            201: CategorySerializer(many=True)
        },  # Returns multiple inserted objects
        tags=["Module 4"],
    )
    def create(self, request):
        # Ensure request contains a list of items
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of objects"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize data (many=True allows multiple objects)
        serializer = CategorySerializer(data=request.data, many=True)

        if serializer.is_valid():
            # Convert validated data to model instances (without saving yet)
            categories = [Category(**item) for item in serializer.validated_data]

            # Use bulk_create() to insert all at once
            created_categories = Category.objects.bulk_create(categories)

            # Serialize the created objects and return response
            return Response(
                CategorySerializer(created_categories, many=True).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####
#  Ex.3v1 A simple ViewSet for updating categories
####


class CategoryUpdateWithSaveViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer,  # Request body structure
        responses={200: CategorySerializer},  # Expected response format
        tags=["Module 4"],
    )
    def update(self, request, pk=None):  # 'pk' is the primary key of the object
        try:
            category = Category.objects.get(pk=pk)  # Fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)  # Validate data

        if serializer.is_valid():
            serializer.save()  # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####
#  Ex.4 A simple ViewSet for updating categories partial updates
####


class CategoryPartialUpdateWithSaveViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer,  # Request body structure
        responses={200: CategorySerializer},  # Expected response format
        tags=["Module 4"],
    )
    def partial_update(self, request, pk=None):  # 'pk' is the primary key of the object
        try:
            category = Category.objects.get(pk=pk)  # Fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category, data=request.data, partial=True
        )  # Validate data

        if serializer.is_valid():
            serializer.save()  # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####
#  Ex.7 API to insert a Product.
####
class ProductInsertViewSet(ViewSet):
    @extend_schema(
        request=CreateProductSerializer,
        responses={201: CreateProductSerializer},
        tags=["Module 4"],
    )
    def create(self, request):
        """
        Creates a Product
        """
        serializer = CreateProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####
#  Ex.8 API to insert a Product and its stock data.
####
class ProductStockInsertViewSet(ViewSet):
    @extend_schema(
        request=CreateProductStockSerializer,
        responses={201: CreateProductStockSerializer},
        tags=["Module 4"],
    )
    def create(self, request):
        """
        Creates a Product and stock record
        """
        serializer = CreateProductStockSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####
# Ex.9 API endpoint to create user and orders with multiple products.
####
class CreateUserViewSet(ViewSet):
    @extend_schema(request=UserSerializer, tags=["Module 4"])
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(ViewSet):
    @extend_schema(
        request=OrderSerializer, responses={201: OrderSerializer}, tags=["Module 4"]
    )
    def create(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####
# Ex.10 Delete.
####


class DeleteCategoryViewSet(ViewSet):
    @extend_schema(tags=["Module 4"])
    def destroy(self, request, pk=None):
        """
        Deletes a category.
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()  # Deletes Order and related OrderProducts due to ForeignKey
            return Response(
                {"message": "Category deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )


####
# Ex.11 Bulk Delete with Custom Action.
####


class BulkDeleteCategoryViewSet(ViewSet):
    @extend_schema(request=CategoryBulkDeleteSerializer, tags=["Module 4"])
    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        Deletes multiple categories based on provided list of category IDs.
        Request body should contain a list of category IDs.
        """

        # Extract the list of category IDs from the request body
        serializer = CategoryBulkDeleteSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            category_ids = serializer.validated_data["ids"]

            if not category_ids:
                return Response(
                    {"error": "No category IDs provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Perform the deletion of the categories
            deleted_count, _ = Category.objects.filter(id__in=category_ids).delete()

            # Return a response indicating how many categories were deleted
            return Response(
                {"message": f"{deleted_count} categories deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            # Return validation errors if serializer is not valid
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
