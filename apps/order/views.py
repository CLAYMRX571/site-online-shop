from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View 
from apps.order.models import Wishlist, Order, OrderItem
from apps.order.forms import WishlistForm
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.

class WishlistCreateView(View):
    def get(self, request, *args, **kwargs):
        data = request.GET
        form = WishlistForm(data)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, f"Mahsulot tanlaganiz qo'shildi")
            return redirect('detail', slug=order.product.slug, size=data.get('size'), color=data.get('color'))

        messages.error(request, f"Mahsulot tanlaganiz qo'shilmadi!!! {form.errors}")
        return redirect('detail', slug=order.product.slug, size=data.get('size'), color=data.get('color'))

class WishlistListAllView(ListView):
    model = Wishlist
    template_name = 'wishlist.html'
    context_object_name = 'wishlists'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class WishlistDeleteView(DeleteView):
    model = Wishlist
    success_url = reverse_lazy("wishlist-all")

class UserOrderView(View):
    def get(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        orderitems = OrderItem.objects.filter(order=order)
        context = {
            'orderitems': orderitems,
            'order': order,
        }
        return render(request, 'cart.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, f"Mahsulotlar buyurtma qilish uchun avval ro'yxatdan o'ting yoki tizimga kiring!")
            return redirect('accounts:login')

        data = request.POST

        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        OrderItem.objects.create(order=order, product_size_id=data.get('product_size'), quantity=data.get('quantity'))

        messages.success(request, f"Mahsulotlar buyurtma qilindi!")
        return redirect('shop')

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("order")

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('order')

class OrderCheckView(View):
    def get(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        orderitems = OrderItem.objects.filter(order=order)
        context = {
            'orderitems': orderitems,
            'order': order,
        }
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, f"Mahsulotlar buyurtma qilish uchun avval ro'yxatdan o'ting yoki tizimga kiring!")
            return redirect('accounts:login')

        data = request.POST

        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        OrderItem.objects.create(order=order, product_size_id=data.get('product_size'), quantity=data.get('quantity'))

        messages.success(request, f"Mahsulotlar buyurtma qilindi!")
        return redirect('shop')