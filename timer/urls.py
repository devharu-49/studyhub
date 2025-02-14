from django.urls import path

from . import views

app_name = "timer"

urlpatterns = [
    path("update_default_time/", views.update_default_time, name="update_default_time"),
    path("save_time/", views.save_time, name="save_time"),
]