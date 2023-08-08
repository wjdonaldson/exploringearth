from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('destinations/', views.DestinationList.as_view(), name='destinations_list'),
  path('destinations/<int:destination_id>/', views.destinations_detail, name='detail'),

  path('accounts/signup/', views.signup, name='signup'),
]
