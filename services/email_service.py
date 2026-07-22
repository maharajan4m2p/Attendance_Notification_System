"""
=========================================================
Attendance Notification System Pro
Email Service
Version : 10.0 Enterprise
Developed by Maharajan
=========================================================
"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    EMAIL_SUBJECT,
    EMAIL_TIMEOUT,
    EMAIL_RETRY_COUNT
)


class EmailService:
    """
    Enterprise Email Service

    Features
    --------
    • SMTP Connection Reuse
    • Batch Email Sending
    • Automatic Reconnection
    • Retry Support
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

        self.timeout = EMAIL_TIMEOUT

        self.retry_count = EMAIL_RETRY_COUNT

        self.connection = None
     
    # =====================================================
    # Connect SMTP Server
    # =====================================================

    def connect(self):

        if self.connection is not None:

            return self.connection

        for attempt in range(

            1,

            self.retry_count + 1

        ):

            try:

                server = smtplib.SMTP(

                    self.smtp_server,

                    self.smtp_port,

                    timeout=self.timeout

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

                print(f"Attempt : {attempt}")

                print("=" * 60)

                return self.connection

            except Exception as error:

                print("=" * 60)

                print(

                    f"SMTP Connection Attempt {attempt} Failed"

                )

                print(error)

                print("=" * 60)

                self.connection = None

        return None
    # =====================================================
    # Disconnect SMTP Server
    # =====================================================

    def disconnect(self):

        if self.connection is None:

            return

        try:

            self.connection.quit()

            print("=" * 60)

            print("SMTP Connection Closed")

            print("=" * 60)

        except Exception as error:

            print("=" * 60)

            print("SMTP Disconnect Failed")

            print(error)

            print("=" * 60)

        finally:

            self.connection = None
            # =====================================================
    # Check SMTP Connection
    # =====================================================

    def is_connected(self):

        if self.connection is None:

            return False

        try:

            status = self.connection.noop()

            return status[0] == 250

        except Exception:

            self.connection = None

            return False
        # =====================================================
    # Reconnect SMTP Server
    # =====================================================

    def reconnect(self):

        print("=" * 60)

        print("Reconnecting SMTP Server...")

        print("=" * 60)

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

            print("Employee email not found.")

            return False

        body = str(
            employee.get(
                "notification",
                ""
            )
        ).strip()

        if not body:

            print(f"No notification found for {email}")

            return False

        subject = employee.get(
            "email_subject",
            self.subject
        )

        if not self.is_connected():

            if self.reconnect() is None:

                return False

        for attempt in range(

            1,

            self.retry_count + 1

        ):

            try:

                message = MIMEMultipart()

                message["From"] = self.username

                message["To"] = email

                message["Subject"] = subject

                message.attach(

                    MIMEText(

                        body,

                        "plain",

                        "utf-8"

                    )

                )

                if self.connection is None:
                    return False
                
                self.connection.sendmail(

                    self.username,

                    email,

                    message.as_string()

                )

                print("=" * 60)

                print(f"Email Sent Successfully : {email}")

                print(f"Attempt : {attempt}")

                print("=" * 60)

                return True

            except Exception as error:

                print("=" * 60)

                print(f"Email Send Failed : {email}")

                print(f"Attempt : {attempt}")

                print(error)

                print("=" * 60)

                self.connection = None

                if attempt < self.retry_count:

                    self.reconnect()

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

        skipped = 0

        print("=" * 60)

        print(f"Sending {total} Emails...")

        print("=" * 60)

        if total == 0:

            return {

                "total": 0,

                "sent": 0,

                "failed": 0,

                "skipped": 0,

                "success_rate": 0

            }

        if not self.is_connected():

            if self.connect() is None:

                return {

                    "total": total,

                    "sent": 0,

                    "failed": total,

                    "skipped": 0,

                    "success_rate": 0

                }

        try:

            for index, employee in enumerate(

                employees,

                start=1

            ):

                if index % 25 == 0 or index == total:

                    progress = round(

                        (index / total) * 100,

                        1

                    )

                    print(

                        f"Processed {index}/{total} ({progress}%)"

                    )

                email = str(

                    employee.get(

                        "email",

                        ""

                    )

                ).strip()

                if not email:

                    skipped += 1

                    continue

                if self.send_email(

                    employee

                ):

                    sent += 1

                else:

                    failed += 1

        finally:

            self.disconnect()

        success_rate = round(

            (sent / total) * 100,

            2

        )

        print("=" * 60)

        print("Email Batch Completed")

        print("=" * 60)

        print(f"Total        : {total}")

        print(f"Sent         : {sent}")

        print(f"Failed       : {failed}")

        print(f"Skipped      : {skipped}")

        print(f"Success Rate : {success_rate}%")

        print("=" * 60)

        return {

            "total": total,

            "sent": sent,

            "failed": failed,

            "skipped": skipped,

            "success_rate": success_rate

        }
        # =====================================================
    # Reset SMTP Connection
    # =====================================================

    def reset(self):

        self.disconnect()

        self.connection = None

        print("=" * 60)

        print("SMTP Connection Reset")

        print("=" * 60)

    # =====================================================
    # Context Manager
    # =====================================================

    def __enter__(self):

        if not self.is_connected():

            self.connect()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        self.disconnect()

        if exc_type is not None:

            print("=" * 60)

            print("SMTP Exception Occurred")

            print(exc_value)

            print("=" * 60)

        return False

    # =====================================================
    # Cleanup
    # =====================================================

    def close(self):

        self.disconnect()

    # =====================================================
    # Destructor
    # =====================================================

    def __del__(self):

        try:

            self.disconnect()

        except Exception:

            pass