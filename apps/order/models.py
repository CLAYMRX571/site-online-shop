from django.db import models
from apps.products.models import Product, Size, Color, ProductSize, BaseModel
from apps.accounts.models import User
# Create your models here.

class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='wishlist')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, related_name='wishlist')

    def __str__(self):
        return f"{self.product}"

ORDER_STATUS = (
    ('Pending', 'pending'),
    ('Ordered', 'ordered'),
)

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=250, default='pending', choices=ORDER_STATUS)

    def __str__(self):
        return f"{self.user}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"

    @property
    def get_total_price(self):
        return self.product_size.price * self.quantity