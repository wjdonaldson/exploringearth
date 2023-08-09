from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("destinations/", views.DestinationList.as_view(), name="destinations_list"),
    path(
        "destinations/<int:pk>/",
        views.DestinationDetail.as_view(),
        name="destinations_detail",
    ),
    path(
        "destinations/create/",
        views.DestinationCreate.as_view(),
        name="destinations_create",
    ),
    path(
        "destinations/<int:pk>/update/",
        views.DestinationUpdate.as_view(),
        name="destinations_update",
    ),
    path(
        "destinations/<int:pk>/delete/",
        views.DestinationDelete.as_view(),
        name="destinations_delete",
    ),
    path(
        "destinations/<int:pk>/add_photo/",
        views.add_photo,
        name="add_photo",
    ),
    path("comments/", views.CommentList.as_view(), name="comments_index"),
    path("comments/<int:pk>/", views.CommentDetail.as_view(), name="comments_detail"),
    path(
        "destinations/<int:destination_id>/comments/create/",
        views.CommentCreate.as_view(),
        name="comments_create",
    ),
    path(
        "comments/<int:pk>/update/",
        views.CommentUpdate.as_view(),
        name="comments_update",
    ),
    path(
        "comments/<int:pk>/delete/",
        views.CommentDelete.as_view(),
        name="comments_delete",
    ),
    path("accounts/signup/", views.signup, name="signup"),
]
