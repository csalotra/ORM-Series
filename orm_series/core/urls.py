from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('prefetch-related/', views.showPrefetchRelated, name='prefetch-realted'),
  path('select-related/', views.showSelectRelated, name='select-related'),
  path('restaurant/', views.restaurant, name='restaurant'),
  path('order/', views.order_product, name='order-product')
]