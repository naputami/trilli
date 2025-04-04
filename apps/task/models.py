from django.contrib.auth.models import User
from django.db import models

from apps.board.models import Board
from core.models import BaseModel


class Task(BaseModel):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        # Add more statuses as needed
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
        null=True,
        blank=True,
    )
    due_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["status"]
