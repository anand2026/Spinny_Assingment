from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, PlacedOrder
from .services import CartService, OrderService


@api_view(['POST'])
def add_item_to_cart(request):
    user_id = request.data.get("user_id")
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    try:
        CartService.add_item_to_cart(user_id, product_id, quantity)
        return Response({"message": "Item added to cart"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_cart(request, user_id):
    try:
        cart_items, total = CartService.get_user_cart(user_id)
        return Response({"cart_items": cart_items, "total": total}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_cart_item(request):
    cart_item_id = request.data.get("cart_item_id")
    quantity = request.data.get("quantity")

    try:
        CartService.update_item_quantity(cart_item_id, quantity)
        return Response({"message": "Cart updated"}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def remove_cart_item(request):
    cart_item_id = request.data.get("cart_item_id")

    try:
        CartService.remove_item(cart_item_id)
        return Response({"message": "Item removed"}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def checkout(request):
    user_id = request.data.get("user_id")
    address_id = request.data.get("address_id")

    try:
        order = OrderService.checkout_cart(user_id, address_id)
        return Response({
            "checkout_id": order.id,
            "total_amount": float(order.total_amount),
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Cart.DoesNotExist:
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def place_order(request):
    checkout_id = request.data.get("checkout_id")

    if not checkout_id:
        return Response({"error": "checkout_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        placed_order = OrderService.place_order(checkout_id)
        return Response({
            "order_id": placed_order.id,
            "status": placed_order.status
        }, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Checkout not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
