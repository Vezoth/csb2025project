from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_user, name="login"),
    path("post/<int:blogpk>", views.blogpost_view, name="postview"),
    path("post/<int:blogpk>/edit", views.editpost, name="editpost"),
    path("post/<int:blogpk>/delete", views.deletepost, name="deletepost"),
    path("post/<int:blogpk>/deletecomment/<int:commentpk>/", views.deletecomment, name="deletecomment"),
]