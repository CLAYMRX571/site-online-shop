from django import forms
from apps.order.models import Wishlist, Order, OrderItem

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ('product', 'color', 'size')