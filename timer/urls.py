from django.urls import path

from . import views

app_name = "timer"

urlpatterns = [
    path("worktime/", views.update_worktime, name="worktime"),
    path("save/", views.save_time, name="save"),
]