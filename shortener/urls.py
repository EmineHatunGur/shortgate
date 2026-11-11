from django.urls import path

from . import views

urlpatterns = [
    path("api/shorten", views.shorten),
    path("health", views.health),
    path("<slug:code>", views.redirect_view),
]
