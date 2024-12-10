from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Brand, Color, Size, Tag, Product, ProductImage, ProductSize, Review
from django.utils.html import format_html
# Register your models here.

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "id"
    list_display_links = ('indented_title', 'id')
    list_display = ['tree_actions', 'indented_title', 'id', 'parent', 'display_icon']
    prepopulated_fields = {"slug": ('name',)}
    
    def display_icon(self, obj):
        return format_html("<img src='%s' style='width: 50px; height: 50px;'>" % obj.icon.url)
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'icons']
    
    def icons(self, obj):
        return format_html("<img src='%s' style='width: 50px; height: 50px;'>" % obj.icon.url)
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color']
    
    def color(self, obj):
        return format_html('<div style="width: 50px; height: 30px; background-color: %s;"></div>' % obj.code)
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductSizeInline(admin.StackedInline):
    model = ProductSize
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline, ProductImageInline ]
    list_display = ['name', 'brand', 'percentage', 'status', 'created_at', ]
    prepopulated_fields = {"slug": ('name',)}
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rate', 'comment']