from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, PlacedOrder


class CartService:
    @staticmethod
    def add_item_to_cart(user_id, product_id, quantity=1):
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        return cart_item

    @staticmethod
    def get_user_cart(user_id):
        user = User.objects.get(id=user_id)
        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return [], 0
            
        items = cart.items.select_related('product').all()
        cart_items = []
        total = 0

        for item in items:
            item_total = item.product.price * item.quantity
            cart_items.append({
                "cart_item_id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": float(item.product.price),
                "item_total": float(item_total),
            })
            total += item_total
            
        return cart_items, total

    @staticmethod
    def update_item_quantity(cart_item_id, quantity):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
            
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    @staticmethod
    def remove_item(cart_item_id):
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()


class OrderService:
    @staticmethod
    def checkout_cart(user_id, address_id):
        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
        items = cart.items.select_related('product').all()
        
        if not items.exists():
            raise ValueError("Cart is empty")
            
        total_amount = sum(item.product.price * item.quantity for item in items)
        
        order = Order.objects.create(
            user=user,
            address_id=address_id,
            total_amount=total_amount,
        )
        
        items.delete()
        return order

    @staticmethod
    def place_order(checkout_id):
        order = Order.objects.get(id=checkout_id)
        
        if hasattr(order, 'placed_order'):
            raise ValueError("Order already placed for this checkout")
            
        placed_order = PlacedOrder.objects.create(
            checkout=order,
            status="CONFIRMED"
        )
        
        order.status = "CONFIRMED"
        order.save()
        return placed_order
