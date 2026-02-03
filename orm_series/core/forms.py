from django import forms
from core.models import Ratings, Restaurant, Order
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductStockException(Exception):
  pass

class RatingForm(forms.ModelForm):
  class Meta:
    model = Ratings
    fields = ('restaurant', 'user', 'rating')

class RestaurantForm(forms.ModelForm):
  class Meta:
    model = Restaurant
    fields = ('name', 'website', 'date_opened', 'latitude', 'longitude', 'restaurant_type')


class ProductOrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ('product', 'number_of_items')

  def save(self, commit=True):
    """To check stock before saving the order"""
    order = super().save(commit=False)
    if order.number_of_items > order.product.number_in_stock:
      raise ProductStockException(
        f"Not enough stock available for this product: {order.product}"
      )
    if commit:
      order.save()
    return order


#Just adding forms.Form
# class RatingForm(forms.Form):
#   rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
