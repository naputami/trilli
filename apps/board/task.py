import logging
import smtplib
import socket

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from huey.contrib.djhuey import task

from .models import Board


@task()
def send_board_invitation(board_id, user_id):
    """Send an email invitation when a user is added to a board"""
    logger = logging.getLogger("huey.consumer")
    try:
        logger.info("Attempting SMTP connection from Huey task...")
        # Test connection first
        server = smtplib.SMTP("smtp.gmail.com", 587)
        logger.info("Connection established")
        server.ehlo()
        logger.info("EHLO successful")
        server.starttls()
        logger.info("STARTTLS successful")
        server.login("nadiapujiutami05@gmail.com", "mkyusvfcjorovolz")
        logger.info("Login successful")
        server.quit()
        logger.info("SMTP test successful")
        board = Board.objects.get(id=board_id)
        user = User.objects.get(id=user_id)

        subject = f"You've been added to {board.title}"
        message = f"""
        Hello {user.username},
        
        You have been added to the board "{board.title}".
        
        Please log in to view the board.
        
        Thanks,
        Task Board Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        print(f"Invitation email sent to {user.email} for board {board.title}")
        return True
    except socket.error as e:
        logger.error(f"Socket error in Huey task: {e}")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error in Huey task: {e}")
        raise
    except Exception as e:
        logger.error(f"Unknown error in Huey task: {e}")
        raise
