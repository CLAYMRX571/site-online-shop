from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from colorfield.fields import ColorField
from apps.accounts.models import User
from apps.common.models import BaseModel
# Create your models here.

class Category(MPTTModel, BaseModel):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icons/')
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Brand(BaseModel):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icons/')

    def __str__(self):
        return self.name
    
class Color(BaseModel):  
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
        ("#0000FF", "blue", ),
        ("#00FF00", "green", ),
    ]
    name = models.CharField(max_length=50)
    code = ColorField(samples=COLOR_PALETTE, default='#FF0000')

    def __str__(self):
        return self.name
    
class Size(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Tag(BaseModel):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
      
class Product(BaseModel):
    STATUS_CHOISES = (
        ('none', 'NONE'),
        ('new', 'NEW'),
        ('hot', 'HOT'),
        ('best', 'BEST SALE'),
    )
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField()
    body = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOISES, default='none')
    percentage = models.FloatField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    categories = models.ManyToManyField(Category, blank=True, related_name="products")
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)    
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    @property
    def get_last_ctg(self):
        return self.categories.last()
    
    @property
    def get_cheap_price(self):
        return self.sizes.order_by('price').first()
    
    @property
    def get_discaunt_price(self):
        return self.get_cheap_price.price - (self.get_cheap_price.price * self.percentage / 100)
    
    @property
    def default_img(self):
        return self.images.first()
    
    @property
    def hover_img(self):
        return self.images.last()
    
    @property
    def get_colors(self):
        return self.sizes.values('color__code', 'color__id').distinct()
    
    @property
    def get_sizes(self):
        return self.sizes.values('size__name', 'size__id').distinct()
    
    @property
    def get_detail_url(self):
        size = self.get_sizes.first()
        color = self.get_colors.first()
        return reverse('detail', kwargs={'slug': self.slug, 'size': size['size__id'], 'color': color['color__id']})

    @property
    def get_url(self):
        size = self.get_sizes.first()
        color = self.get_colors.first()
        return reverse('compare', kwargs={'slug': self.slug, 'size': size['size__id'], 'color': color['color__id']})

class ProductSize(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='sizes')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, related_name='sizes')
    availability = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product} - {self.size} - {self.color}"

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.product}"
    
    @property
    def image_url(self):
        return self.image.url

class Review(BaseModel):  
    RATING_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),

    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rate = models.IntegerField(choices=RATING_CHOICES, default=1)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product} | {self.user} | {self.rate}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = "Reviews"

    @property
    def stars_percent(self):
        return round(int(self.rate * 100 / 5), 1)