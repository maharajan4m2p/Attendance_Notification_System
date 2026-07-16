"""
=========================================================
Email Service
Developed by Maharajan
=========================================================
"""

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_ADDRESS,
    EMAIL_PASSWORD
)

from services.email_template import EmailTemplate


class EmailService:

    def __init__(self):

        self.template = EmailTemplate()

    def send_email(self, employee):

        try:

            subject, body = self.template.generate(employee)

            message = MIMEMultipart()

            message["From"] = EMAIL_ADDRESS

            message["To"] = employee["email"]

            message["Subject"] = subject

            message.attach(
                MIMEText(body, "plain")
            )

            server = smtplib.SMTP(
                SMTP_SERVER,
                SMTP_PORT
            )

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.sendmail(
                EMAIL_ADDRESS,
                employee["email"],
                message.as_string()
            )

            server.quit()

            return True

        except Exception as e:

            print(e)

            return False
        