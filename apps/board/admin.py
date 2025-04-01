from django.contrib import admin
from .models import Board, BoardMember

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
       list_display = (
        "title",
        "description",
        "actor",
        "created_at",
        "updated_at",
    )

@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
        list_display = (
        "board",
        "user",
        "role",
        "joined_at"
    )


