from django.urls import path
from . import views

urlpatterns = [
    path('add-item/', views.add_item_to_cart, name='add-item-to-cart'),
    path('<int:user_id>/', views.get_cart, name='get-cart'),
    path('update-item/', views.update_cart_item, name='update-cart-item'),
    path('remove-item/', views.remove_cart_item, name='remove-cart-item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place/', views.place_order, name='place-order'),
]
