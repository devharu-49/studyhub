from django.urls import path
from .views import (
    tasklist_view,
    taskdetail_view,
    taskcreate_view,
    taskdelete_view,
    taskedit_view,
    statusedit_view,
    tasksearch_view,
)


urlpatterns = [
    path("", tasklist_view, name="task_list"),
    path("<int:id>/", taskdetail_view, name="task_detail"),
    path("form/", taskcreate_view, name="task_create"),
    path("delete/<int:id>/", taskdelete_view, name="task_delete"),
    path("edit/<int:id>/", taskedit_view, name="task_edit"),
    path("status/<int:id>/", statusedit_view, name="status_edit"),
    path("task/search/", tasksearch_view, name="task_search"),
]
