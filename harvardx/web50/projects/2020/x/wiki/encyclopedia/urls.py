from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.Html_page, name="Html_page"),
    path("create", views.create_page, name="create_page"),
    path("edit", views.edit_page, name="edit_page"),
    path("save_edit", views.save_edit, name="save_edit"),
    path("search",views.search, name="search"),
    path("random",views.random, name="random")
]
