"""
=========================================================
Attendance Notification System Pro
Email Service
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    EMAIL_SUBJECT
)


class EmailService:
    """
    Enterprise Email Service

    Features
    --------
    • SMTP Connection Reuse
    • Batch Email Sending
    • Auto Reconnect
    • Context Manager Support
    • Enterprise Performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.smtp_server = SMTP_SERVER

        self.smtp_port = SMTP_PORT

        self.username = SMTP_USERNAME

        self.password = SMTP_PASSWORD

        self.subject = EMAIL_SUBJECT

        self.connection = None

    # =====================================================
    # Connect SMTP Server
    # =====================================================

    def connect(self):

        if self.connection is not None:

            return self.connection

        try:

            server = smtplib.SMTP(

                self.smtp_server,

                self.smtp_port,

                timeout=30

            )

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(

                self.username,

                self.password

            )

            self.connection = server

            print("=" * 60)
            print("SMTP Connected Successfully")
            print("=" * 60)

            return self.connection

        except Exception as error:

            print("=" * 60)
            print(
                f"SMTP Connection Failed : {error}"
            )
            print("=" * 60)

            self.connection = None

            return None

    # =====================================================
    # Disconnect SMTP
    # =====================================================

    def disconnect(self):

        if self.connection is None:

            return

        try:

            self.connection.quit()

        except Exception:

            pass

        finally:

            self.connection = None

            print("=" * 60)
            print("SMTP Connection Closed")
            print("=" * 60)

    # =====================================================
    # Check SMTP Connection
    # =====================================================

    def is_connected(self):

        if self.connection is None:

            return False

        try:

            self.connection.noop()

            return True

        except Exception:

            self.connection = None

            return False

    # =====================================================
    # Reconnect SMTP
    # =====================================================

    def reconnect(self):

        self.disconnect()

        return self.connect()
    # =====================================================
    # Send Email
    # =====================================================

    def send_email(
        self,
        employee
    ):

        email = str(
            employee.get(
                "email",
                ""
            )
        ).strip()

        if not email:

            return False

        body = str(
            employee.get(
                "notification",
                ""
            )
        ).strip()

        if not body:

            return False

        if not self.is_connected():

            if self.reconnect() is None:

                return False

        try:

            message = MIMEMultipart()

            message["From"] = self.username

            message["To"] = email

            message["Subject"] = self.subject

            message.attach(

                MIMEText(

                    body,

                    "plain",

                    "utf-8"

                )

            )

            self.connection.sendmail(

                self.username,

                email,

                message.as_string()

            )

            return True

        except Exception as error:

            print("=" * 60)
            print(
                f"Email Failed : {email}"
            )
            print(error)
            print("=" * 60)

            self.connection = None

            return False

    # =====================================================
    # Send Batch Emails
    # =====================================================

    def send_batch(
        self,
        employees
    ):

        total = len(employees)

        sent = 0

        failed = 0

        print("=" * 60)
        print(
            f"Sending {total} Emails..."
        )
        print("=" * 60)

        if not self.is_connected():

            self.connect()

        try:

            for index, employee in enumerate(

                employees,

                start=1

            ):

                if index % 100 == 0 or index == total:

                    progress = round(

                        index * 100 / total,

                        1

                    )

                    print(

                        f"Processed {index}/{total} ({progress}%)"

                    )

                if self.send_email(

                    employee

                ):

                    sent += 1

                else:

                    failed += 1

        finally:

            self.disconnect()

        success_rate = round(

            sent * 100 / total,

            2

        ) if total else 0

        print("=" * 60)
        print("Email Batch Completed")
        print("=" * 60)

        print(f"Total        : {total}")
        print(f"Sent         : {sent}")
        print(f"Failed       : {failed}")
        print(f"Success Rate : {success_rate}%")

        print("=" * 60)

        return {

            "total": total,

            "sent": sent,

            "failed": failed,

            "success_rate": success_rate

        }

    # =====================================================
    # Reset SMTP Connection
    # =====================================================

    def reset(self):

        self.disconnect()

        self.connection = None

    # =====================================================
    # Context Manager
    # =====================================================

    def __enter__(self):

        self.connect()

        return self

    def __exit__(

        self,

        exc_type,

        exc_value,

        traceback

    ):

        self.disconnect()

    # =====================================================
    # Cleanup
    # =====================================================

    def close(self):

        self.disconnect()
        