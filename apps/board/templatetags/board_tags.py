from django import template

register = template.Library()


@register.filter
def user_role(board, user):
    return board.get_user_role(user)
