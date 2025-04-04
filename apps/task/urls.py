from django.urls import path

from .views import CreateTaskView, TaskListView

urlpatterns = [
    path("boards/<str:board_id>/tasks/", TaskListView.as_view(), name="task_list"),
    path(
        "boards/<str:board_id>/tasks/create",
        CreateTaskView.as_view(),
        name="create_task",
    ),
]
