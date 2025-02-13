from django.urls import path
from .views import tasklist_view, taskdetail_view

urlpatterns = [
    path("", tasklist_view, name="tasklist"),
    path("<int:id>/", taskdetail_view, name="taskdetail"),
]
