from django.urls import path
from . import views
from apps.products.views import HomeProductsListView, ProductDetailView, ShopListView, ShopCompareView, AboutView, BlogListView, PrivacyView, GuideView, TermsView, FilterView, Error404View, lan_switch

urlpatterns = [
    path('', HomeProductsListView.as_view(), name='index'),
    path('product/<slug:slug>/<int:size>/<int:color>/', ProductDetailView.as_view(), name='detail'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('compare/<slug:slug>/<int:size>/<int:color>/', ShopCompareView.as_view(), name='compare'),
    path('about/', AboutView.as_view(), name='about'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('guide/', GuideView.as_view(), name='guide'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('filter/', FilterView.as_view(), name='filter'),
    path('error/', Error404View.as_view(), name='error'),
    path('lan/<str:lan>/', lan_switch, name='lan_switch'),
]