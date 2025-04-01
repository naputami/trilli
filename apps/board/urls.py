from django.urls import path
from .views import BoardListView, CreateBoardView, EditBoardView, DeleteBoardView, BoardMemberView, AddBoardMemberView, DeleteMemberView

urlpatterns = [
    path("", BoardListView.as_view(), name="board"),
    path("boards/create/", CreateBoardView.as_view(), name="create_board"),
    path("boards/<str:id>/edit/", EditBoardView.as_view(), name="edit_board"),
    path("boards/<str:id>/delete/", DeleteBoardView.as_view(), name="delete_board"),
    path("boards/<str:id>/members/", BoardMemberView.as_view(), name="board_member"),
    path("boards/<str:id>/members/create/", AddBoardMemberView.as_view(), name="add_member"),
    path("boards/<str:board_id>/members/<str:membership_id>/delete/", DeleteMemberView.as_view(), name="delete_member"),
]
