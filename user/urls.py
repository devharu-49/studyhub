from django.urls import path
from .views import base_view, signup_view, login_view

urlpatterns = [
    path("base/", base_view, name="base"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
]
