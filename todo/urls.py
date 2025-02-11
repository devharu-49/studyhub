from django.urls import path
from .views import tasklist_view

urlpatterns = [
    path("", tasklist_view, name="tasklist"),
]
