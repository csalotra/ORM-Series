from django import forms
from core.models import Ratings, Restaurant
from django.core.validators import MinValueValidator, MaxValueValidator

class RatingForm(forms.ModelForm):
  class Meta:
    model = Ratings
    fields = ('restaurant', 'user', 'rating')

class RestaurantForm(forms.ModelForm):
  class Meta:
    model = Restaurant
    fields = ('name', 'website', 'date_opened', 'latitude', 'longitude', 'restaurant_type')


#Just adding forms.Form
# class RatingForm(forms.Form):
#   rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
