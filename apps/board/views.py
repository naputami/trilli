from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from core.views import LoginRequiredViewMixin

from .forms import BoardForm, BoardMemberForm
from .models import Board, BoardMember
from .task import send_board_invitation_task


# Create your views here.
class BoardListView(LoginRequiredViewMixin, ListView):
    model = Board
    template_name = "board_list.html"
    context_object_name = "boards"
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(actor=user) | Q(members__user=user)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class CreateBoardView(LoginRequiredViewMixin, View):
    def get(self, request):
        form = BoardForm()
        return render(request, "create_board.html", {"form": form})

    def post(self, request):
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.actor = request.user
            board.save()

            BoardMember.objects.create(board=board, user=request.user, role="admin")

            return redirect("board")
        else:
            return render(request, "create_board.html", {"form": form})


class EditBoardView(LoginRequiredViewMixin, View):
    def get(self, request, id):
        board = get_object_or_404(Board, id=id)
        form = BoardForm(instance=board)
        return render(request, "edit_board.html", {"form": form})

    def post(self, request, id):
        board = get_object_or_404(Board, id=id)
        form = BoardForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            board.title = title
            board.description = description

            board.save()
            return redirect("board")
        else:
            return render(request, "edit_board.html", {"form": form})


class DeleteBoardView(LoginRequiredViewMixin, View):
    def post(self, request, id):
        board = get_object_or_404(Board, id=id)
        board.delete()

        return redirect("board")


class BoardMemberView(LoginRequiredViewMixin, View):
    def get(self, request, id):
        board = get_object_or_404(Board, id=id)
        members = BoardMember.objects.filter(board=board)

        return render(
            request, "board_member.html", {"members": members, "board": board}
        )


class AddBoardMemberView(LoginRequiredViewMixin, View):
    def get(self, request, id):
        board = get_object_or_404(Board, id=id)
        form = BoardMemberForm()
        return render(request, "add_member.html", {"form": form, "board": board})

    def post(self, request, id):
        board = get_object_or_404(Board, id=id)

        if board.get_user_role(request.user) != "admin":
            return HttpResponseForbidden("Only board admins can add members.")

        form = BoardMemberForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            role = form.cleaned_data["role"]

            user = User.objects.get(email=email)
            

            try:
                if board.is_member(user):
                    messages.warning(
                        request, f"{user.username} is already a member of this board."
                    )
                else:
                    BoardMember.objects.create(board=board, user=user, role=role)
                    send_board_invitation_task(board.id, user.id)
                    return redirect("board_member", id=board.id)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return render(request, "add_member.html", {"form": form, "board": board})
        else:
            return render(request, "add_member.html", {"form": form, "board": board})


class DeleteMemberView(LoginRequiredViewMixin, View):
    def post(self, request, board_id, membership_id):
        board = get_object_or_404(Board, id=board_id)
        membership = get_object_or_404(BoardMember, id=membership_id, board=board)

        if board.get_user_role(request.user) != "admin":
            return HttpResponseForbidden("Only board admins can remove members.")

        membership.delete()

        return redirect("board_member", id=board.id)
