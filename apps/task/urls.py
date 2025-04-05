from django.urls import path

from .views import CreateTaskView, DeleteTaskView, EditTaskView, TaskListView

urlpatterns = [
    path("boards/<str:board_id>/tasks/", TaskListView.as_view(), name="task_list"),
    path(
        "boards/<str:board_id>/tasks/create",
        CreateTaskView.as_view(),
        name="create_task",
    ),
    path(
        "boards/<str:board_id>/tasks/<str:task_id>/edit/",
        EditTaskView.as_view(),
        name="edit_task",
    ),
    path(
        "boards/<str:board_id>/tasks/<str:task_id>/delete/",
        DeleteTaskView.as_view(),
        name="delete_task",
    ),
]
