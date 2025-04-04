import smtplib
import socket

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    print("Connection established")
    server.ehlo()
    print("EHLO successful")
    server.starttls()
    print("STARTTLS successful")
    server.login(
        "nadiapujiutami05@gmail.com", "mkyusvfcjorovolz"
    )  # Replace with your credentials
    print("Login successful")
    server.quit()
    print("SMTP connection test successful")
except socket.error as e:
    print(f"Socket error: {e}")
except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")
