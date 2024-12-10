from django.contrib import admin
from apps.order.models import Wishlist, Order, OrderItem
# Register your models here.

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'color', 'size']
    list_filter = ['user', 'product', 'color', 'size']
    search_fields = ['user', 'product', 'color', 'size']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['user', 'status']
    list_filter = ['user', 'status']
    search_fields = ['user', 'status']