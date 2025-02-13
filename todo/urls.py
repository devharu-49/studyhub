from django.urls import path
from .views import tasklist_view, taskdetail_view, taskcreate_view


urlpatterns = [
    path("", tasklist_view, name="task_list"),
    path("<int:id>/", taskdetail_view, name="task_detail"),
    path("form/", taskcreate_view, name="task_create"),
]
