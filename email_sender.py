import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipient, subject, message):
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email sending failed:", e)
        return False
