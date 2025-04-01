from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel


class Board(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def get_member_count(self):
        return self.members.count()

    def is_member(self, user):
        return self.members.filter(user=user).first()

    def get_user_role(self, user):
        try:
            member = self.members.get(user=user)
            return member.role
        except BoardMember.DoesNotExist:
            return None


class BoardMember(BaseModel):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("editor", "Editor"),
        ("viewer", "Viewer"),
    ]

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="members",
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="board_memberships",
        null=False,
        blank=False,
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="viewer")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["board", "user"]
