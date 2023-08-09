from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
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


class DestinationDetail(DetailView):
  model = Destination
  fields = ['name', 'description', 'location', 'user']


class DestinationCreate(CreateView):
  model = Destination
  fields = ['name', 'description', 'location']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class DestinationUpdate(UpdateView):
  model = Destination
  fields = ['name', 'description', 'location']


class DestinationDelete(DeleteView):
  model = Destination
  success_url = '/destinations'


class CommentList(ListView):
  model = Comment
  fields = ["comment", "timestamp", "user", "destination"]


class CommentDetail(DetailView):
  model = Comment
  fields = ["comment", "timestamp", "user", "destination"]


class CommentCreate(CreateView):
  model = Comment
  fields = ["comment", "destination"]

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class CommentUpdate(UpdateView):
  model = Comment
  fields = ["comment"]


class CommentDelete(DeleteView):
  model = Comment
  success_url = '/destinations'

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