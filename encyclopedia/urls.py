from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new_entry", views.new_entry, name="new_entry"),
    path("wiki/random",views.random, name="random"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
]
