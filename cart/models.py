from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class PlacedOrder(models.Model):
    checkout = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='placed_order')
    status = models.CharField(max_length=20, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PlacedOrder #{self.id} for Checkout #{self.checkout.id}"
