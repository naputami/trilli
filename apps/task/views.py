from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from apps.board.models import Board
from core.views import LoginRequiredViewMixin

from .forms import TaskForm
from .models import Task

# Create your views here.


class TaskListView(LoginRequiredViewMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        self.board = get_object_or_404(Board, id=self.kwargs["board_id"])
        if self.board.is_member(self.request.user):
            return Task.objects.filter(board=self.board)
        else:
            return HttpResponseForbidden("You dont have access to this board")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.board
        return context


class CreateTaskView(LoginRequiredViewMixin, View):
    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        form = TaskForm(request=request, board=board)
        return render(request, "create_task.html", {"form": form, "board": board})

    def post(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)

        if (
            board.get_user_role(request.user) != "admin"
            and board.get_user_role(request.user) != "editor"
        ):
            return HttpResponseForbidden(
                "Only board admins and editor can create tasks"
            )

        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.actor = request.user
            task.board = board
            task.save()

            messages.success(request, "Task created successfully!")
            return redirect("task_list", board_id=board.id)
        else:
            return render(request, "create_task.html", {"form": form, "board": board})
