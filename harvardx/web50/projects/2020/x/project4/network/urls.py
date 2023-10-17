from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost", views.createpost, name="createpost"),
    path("user/<int:user_id>", views.user, name="user"),
    path("followuser/<int:user_id>",views.followuser, name="followuser"),
    path("unfollowuser/<int:user_id>",views.unfollowuser, name="unfollowuser"),
    path("following", views.following, name="following"),
    path("editpost/<int:post_id>",views.editpost, name="editpost"),
    path("likepost/<int:post_id>",views.likepost,name="likepost"),
    path("unlikepost/<int:post_id>",views.unlikepost,name="unlikepost"),

]