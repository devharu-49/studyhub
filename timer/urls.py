from django.urls import path

from . import views

app_name = "timer"

urlpatterns = [
    path("update/", views.update_settime, name="update"),
    path("save/", views.save_time, name="save"),
]