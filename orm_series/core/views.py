from django.shortcuts import render
from .forms import RatingForm, RestaurantForm

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

def restaurant(request):
    if request.method == 'POST':
      form = RestaurantForm(request.POST or None)
      if form.is_valid(): #is_valid check the validators
        print(form.cleaned_data)
        # form.save()
      else:
        return render(request, 'index.html', {'form': form})
    context = {'form': RestaurantForm()}
    return render(request, 'index.html', context)


