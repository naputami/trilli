from huey.contrib.djhuey import task
from .methods import send_board_invitation


@task()
def send_board_invitation_task(board_id, user_id):
    send_board_invitation(board_id, user_id)
