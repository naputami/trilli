from django import forms
from django.contrib.auth import get_user_model

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "assigned_to", "due_date"]
        widgets = {
            "due_date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "input input-bordered w-full"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Task description",
                    "class": "textarea h-24 w-full",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Task title",
                }
            ),
            "status": forms.Select(attrs={"class": "select w-full"}),
            "assigned_to": forms.Select(attrs={"class": "select w-full"}),
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop("board", None)
        request = kwargs.pop("request", None)
        super(TaskForm, self).__init__(*args, **kwargs)

        User = get_user_model()

        if board:
            members_queryset = User.objects.filter(
                id__in=board.members.all().values_list("user_id", flat=True)
            ).order_by("first_name", "last_name")

            if self.instance and self.instance.assigned_to:
                members_queryset = members_queryset | User.objects.filter(
                    id=self.instance.assigned_to.id
                )

            self.fields["assigned_to"].queryset = members_queryset

        if request and "status" in request.GET:
            self.fields["status"].initial = request.GET.get("status")
