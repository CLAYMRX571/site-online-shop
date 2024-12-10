from django.urls import path
from apps.order.views import WishlistCreateView, WishlistListAllView, WishlistDeleteView, UserOrderView, OrderDeleteView, OrderItemDeleteView, OrderCheckView

urlpatterns = [
    path('wishlist/', WishlistCreateView.as_view(), name='wishlist'),
    path('wishlist/all/', WishlistListAllView.as_view(), name='wishlist-all'),
    path('wishlist/<pk>/delete/', WishlistDeleteView.as_view(), name='delete'),
    path('cart/', UserOrderView.as_view(), name='order'),
    path('cart/<pk>/delete/', OrderItemDeleteView.as_view(), name='order-delete'),
    path('cart/<pk>/clear/', OrderDeleteView.as_view(), name='clear'),
    path('check/', OrderCheckView.as_view(), name='checkout'),
]