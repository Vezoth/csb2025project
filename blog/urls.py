from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_user, name="login"),
    path("post/<int:blogpk>", views.blogpost_view, name="postview")
]