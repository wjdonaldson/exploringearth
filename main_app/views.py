import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Destination, Comment, Photo


# Create your views here.
def home(request):
     # Getting all the stuff from database
    destinations = Destination.objects.all();

    # Creating a dictionary to pass as an argument
    context = { 'destinations' : destinations }

    # Returning the rendered html
    return render(request, "home.html", context)
    #return render(request, "home.html")

def about(request):
    return render(request, "about.html")


class DestinationList(LoginRequiredMixin, ListView):
    model = Destination
    fields = ["name", "description", "location", "user"]


class DestinationDetail(LoginRequiredMixin, DetailView):
    model = Destination
    fields = ["name", "description", "location", "user"]


class DestinationCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Destination
    fields = ["name", "description", "location"]

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("/")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DestinationUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Destination
    fields = ["name", "description", "location"]

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("/")


class DestinationDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Destination
    success_url = "/destinations"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("/")


class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    fields = ["comment", "timestamp", "user", "destination"]


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    fields = ["comment", "timestamp", "user", "destination"]


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["comment"]

    def form_valid(self, form):
        form.instance.destination_id = self.kwargs["destination_id"]
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["comment"]


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = "/destinations"

@login_required
def add_photo(request, destination_id):
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind(".") :]
        try:
            bucket = os.environ["S3_BUCKET"]
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, destination_id=destination_id)
        except Exception as e:
            print("An error occurred uploading file to S3")
            print(e)
    return redirect("destinations_detail", pk=destination_id)

def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)

class PhotoList(LoginRequiredMixin, ListView):
    model = Photo

