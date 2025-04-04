from django.contrib import admin

from .models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "assigned_to",
        "due_date",
        "status",
        "actor",
        "created_at",
        "updated_at",
    )
