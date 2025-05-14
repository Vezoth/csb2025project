from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("login/",  auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("settings/", views.settings, name="settings"),
    path("register/", views.register, name="register"),
    path("posts/<int:blogpk>", views.blogpost_view, name="postview"),
    path("posts/<int:blogpk>/edit", views.editpost, name="editpost"),
    path("posts/<int:blogpk>/delete", views.deletepost, name="deletepost"),
    path("posts/<int:blogpk>/deletecomment/<int:commentpk>", views.deletecomment, name="deletecomment"),
    path("posts/new", views.newpost, name="newpost"),
]