import logging
from mailjet_rest import Client
import os
from dotenv import load_dotenv
from apps.board.models import Board
from django.contrib.auth.models import User

load_dotenv(override=True)

api_key = os.environ.get('MJ_APIKEY_PUBLIC')
api_secret = os.environ.get('MJ_APIKEY_PRIVATE')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_board_invitation(board_id, user_id):
    logger = logging.getLogger("huey.consumer")
    try:
        board = Board.objects.get(id=board_id)
        user = User.objects.get(id=user_id)

        subject = f"You've been added to {board.title}"
        message_text = f"""
        Hello {user.username},
        
        You have been added to the board "{board.title}".
        
        Please log in to view the board.
        
        Thanks,
        Trilli Team
        """
        message_html = f""" 
         <p style="margin: 0 0 16px 0;">Hello {user.username},</p>
         <p style="margin: 0 0 16px 0;">You have been added to the board <strong style="font-weight: bold;">"{board.title}"</strong>.</p>
         <p style="margin: 0 0 16px 0;">Please log in to view the board.</p>
         <div style="margin-top: 20px; color: #777777; font-size: 0.9em;">
            <p style="margin: 0;">Thanks,<br>
            <strong style="font-weight: bold;">Trilli Team</strong></p>
         </div>
        """
        data = {
            'Messages': [
                            {
                                    "From": {
                                            "Email": "nadiapujiutami14@gmail.com",
                                            "Name": "Trilli Team"
                                    },
                                    "To": [
                                            {
                                                    "Email": user.email,
                                                    "Name": f'{user.first_name} {user.last_name}'
                                            }
                                    ],
                                    "Subject": subject,
                                    "TextPart": message_text,
                                    "HTMLPart": message_html
                            }
                    ]
        }
        result = mailjet.send.create(data=data)
        logger.info(result.status_code)
        logger.info(result.json())
    except Exception as e:
        logger.error(f"Unknown error in Huey task: {e}")