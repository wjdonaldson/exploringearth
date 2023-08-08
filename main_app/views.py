from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Destination, Comment, Photo


# Create your views here.
def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


class DestinationList(ListView):
  model = Destination
  fields = ['name', 'description', 'location', 'user']


def destinations_detail(request, destination_id):
  destination = Destination.objects.get(id=destination_id)
  return render(request, 'destinations/detail.html', {'destination': destination})


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)