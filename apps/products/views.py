from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.products.models import Product, Category, ProductSize, Tag, Brand, Size, Color, ProductImage, Review
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.

class HomeProductsListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'featured_products'
    ordering = ['-id']
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_active=True).order_by('?')[:8]
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        featured_products = Product.objects.filter(is_active=True).order_by('-id')[:5]
        context['featured_products'] = featured_products
        popular_products = Product.objects.filter(is_active=True).order_by('id')[:5]
        context['popular_products'] = popular_products
        new_added_products = Product.objects.filter(is_active=True).order_by('?')[:5]
        context['new_added_products'] = new_added_products
        new_arrivals_products = Product.objects.filter(is_active=True).order_by('?')[:4]
        context['new_arrivals_products'] = new_arrivals_products
        brand = Brand.objects.filter(is_active=True)
        context['brand'] = brand
        deals_products = Product.objects.filter(is_active=True).order_by('id')[:3]
        context['deals_products'] = deals_products
        top_selling_products = Product.objects.filter(is_active=True).order_by('-id')[:3]
        context['top_selling_products'] = top_selling_products
        hot_products = Product.objects.filter(is_active=True).order_by('?')[:3]
        context['hot_products'] = hot_products
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'
    lookup_field = 'slug'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        size = ProductSize.objects.get(size__id=self.kwargs.get('size'), product=self.object)
        color = Color.objects.get(id=self.kwargs.get('color'))
        images = ProductImage.objects.filter(product=self.object, color=color)
        related_products = Product.objects.filter(categories__in=self.object.categories.all()).exclude(id=self.object.id).order_by('?')[:4]
        reviewes = self.object.reviews.all()
        context['reviewes'] = reviewes
        context['related_products'] = related_products
        context['active_size'] = size
        context['active_color'] = color
        context['active_images'] = images
        return context

class ShopListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'page_obj'
    page_size = 10
    ordering = ['?']

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset().filter(is_active=True)
        category = self.request.GET.get('category')
        statuses = self.request.GET.getlist('status')
        if category:
            queryset = queryset.filter(categories__id=category)

        if statuses:
            queryset = queryset.filter(status__in=statuses)

        paginator = Paginator(queryset, self.page_size)
        page_num = self.request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        return page_obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            context['active_category'] = Category.objects.get(id=category)

        context['brand'] = Brand.objects.filter(is_active=True)
        return context

class ShopCompareView(DetailView):
    model = Product
    template_name = 'compare.html'
    context_object_name = 'compare'
    lookup_field = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        size = ProductSize.objects.get(size__id=self.kwargs.get('size'), product=self.object)
        color = Color.objects.get(id=self.kwargs.get('color'))
        images = ProductImage.objects.filter(product=self.object, color=color)
        related_products = Product.objects.filter(categories__in=self.object.categories.all()).exclude(id=self.object.id)
        reviewes = self.object.reviews.all()
        context['reviewes'] = reviewes
        context['related_products'] = related_products
        context['active_size'] = size
        context['active_color'] = color
        context['active_images'] = images
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class BlogListView(ListView):
    model = Product 
    template_name = 'blog.html'
    context_object_name = 'blog'
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_active=True)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.filter(is_active=True)
        context['tag'] = tag
        return context

def contact(request,):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        email = EmailMessage(
            subject="Sizga xabar keldi",
            body=f"""
            {first_name}
            {last_name}
            {email}
            {phone}
            {message}
            """,
            to=['onlineshop571632@gmail.com'],
            )
        email.send()

    return render(request, 'contact.html')

class GuideView(TemplateView):
    template_name = 'guide.html'

class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class GuideView(TemplateView):
    template_name = 'guide.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

class FilterView(TemplateView):
    template_name = 'filter.html'

class Error404View(TemplateView):
    template_name = '404.html'

def lan_switch(request, lan):
    return redirect(f'/{lan}/')