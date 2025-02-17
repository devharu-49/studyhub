from django.urls import path

from . import views

app_name = "timer"

urlpatterns = [
    path("default/", views.update_default_time, name="default"),
    path("save/", views.save_time, name="save"),
]