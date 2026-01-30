from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower

# Custom Validator
def validate_restaurant_name_begins_with_capitals(value):
  if not value or not value[0].isupper():
    raise ValidationError('Restaurant name must begin with capital letters')

class Restaurant(models.Model):
  class TypeChoices(models.TextChoices):
    INDIAN = 'IN', 'Indian'
    CHINESE = 'CH', 'Chinese'
    ITALIAN = 'IT', 'Italian'
    GREEK = 'GR', 'Greek'
    MEXICAN = 'MX', 'Mexican'
    FASTFOOD = 'FF', 'Fast Food'
    OTHER = 'OT', 'Other'


  name = models.CharField(max_length=100, validators=[validate_restaurant_name_begins_with_capitals])
  website = models.URLField(default='')
  date_opened = models.DateField()
  latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
  longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
  restaurant_type = models.CharField(max_length=2, choices=TypeChoices.choices)

  class Meta:
    ordering = [Lower('name')] #default ordering
    get_latest_by = 'date_opened' #default field when we call .earliest() or .latest()

  def __str__(self):
    return self.name
  
  def save (self, *args, **kwargs):
    print(self._state.adding) # Here we can add any logic we want to execute before save executes
    super().save(*args, **kwargs)

class Staff(models.Model):
  name = models.CharField(max_length=128)
  restaurants = models.ManyToManyField(Restaurant, through="StaffRestaurant")

  def __str__(self):
    return self.name
  
class StaffRestaurant(models.Model):
  staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  salary = models.FloatField(null=True, blank=True)
  date_joined = models.DateField()
  is_manager = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.staff.name} - {self.restaurant.name}"  
  
class Ratings(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="ratings")
  rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

  def __str__(self):
    return f"rating: {self.rating}"
  
class Sale(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name="sales")
  income = models.DecimalField(max_digits=8, decimal_places=2)
  datetime = models.DateTimeField()


  

