from django.shortcuts import render
from django.utils import timezone
from .forms import RatingForm, RestaurantForm
from core.models import Restaurant, Sale, Ratings
from django.db.models import Prefetch, Sum

def index(request):
  if request.method == 'POST':
    form = RatingForm(request.POST or None)
    if form.is_valid(): #is_valid check the validators
      # print(form.cleaned_data)
      form.save()
    else:
      return render(request, 'index.html', {'form': form})
  context = {'form': RatingForm()}
  return render(request, 'index.html', context)

"""
To check N+1 problem

-> For foreignkey backward(i.e. restaurant to ratings) relations and Many-to-many relations we use prefetch_related
-> For foreignkey forward(i.e. ratings to restaurant) relations and One-to-one relations we use select_related

""" 
def showPrefetchRelated(request):
  #  restaurants = Restaurant.objects.all() # uncomment this to check the N+1 case

  ## prefetch_related  (Execute two queries not N+1)
  #  restaurants = Restaurant.objects.prefetch_related('ratings')  # uncomment this to test the prefetch_related

  ## Prefetch: to filter the backward 
  #  restaurants = Restaurant.objects.prefetch_related(Prefetch("ratings", queryset=Ratings.objects.filter(rating__gt=2)))  #If you want to fetch only ratings that are greater than 2 

  ## Prefetch from 2 models
  #  restaurants = Restaurant.objects.prefetch_related('ratings', 'sales') #uncomment the other for loop for sales in the prefetches.html

  ## Filters and Prefetch 
  #  restaurants = Restaurant.objects.filter(name__istartswith = 'c').prefetch_related('ratings', 'sales') 

    # restaurants = Restaurant.objects.prefetch_related('ratings', 'sales') \
    #   .filter(ratings__rating__gt=2) \
    #   .annotate(total = Sum('sales__income'))

  ## Filter Object
    # restaurants = Restaurant.objects.filter(name__istartswith = 'c').prefetch_related(
    #     Prefetch("ratings", queryset=Ratings.objects.filter(rating__gt=2)),
    #     Prefetch("sales", queryset=Sale.objects.filter(income__gt=100))
    # )

    month_ago = timezone.now() - timezone.timedelta(days=30)
    monthly_sales = Prefetch("sales", queryset=Sale.objects.filter(datetime__gte=month_ago))

    restaurants = Restaurant.objects.prefetch_related('ratings', monthly_sales)\
    .filter(ratings__rating__gt=2)

    restaurants = restaurants.annotate(total=Sum('sales__income'))

    context = {'restaurants': restaurants}
    return render(request, 'prefetches.html', context)



def showSelectRelated(request):
  
  #  ratings = Ratings.objects.select_related("restaurant")

  ## .Only : it select only the mentioned fields, .defer(), it does not select the mentioned fields 
  ## These two .defer and .only needs to be executed with CAUTION, as if tried to access any other fields than mentioned will cause N+1 queries in the background

  ratings = Ratings.objects.only("rating", "restaurant__name" ).select_related('restaurant')
  context = {'ratings': ratings}
  return render(request, 'selects.html', context)


def restaurant(request):
    if request.method == 'POST':
      form = RestaurantForm(request.POST or None)
      if form.is_valid(): #is_valid check the validators
        # print(form.cleaned_data)
        form.save()
      else:
        return render(request, 'index.html', {'form': form})
    context = {'form': RestaurantForm()}
    return render(request, 'index.html', context)


