"""
=========================================================
Attendance Notification System Pro
Enterprise Email Service
Version : 13.0 Enterprise
=========================================================
"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    COMPANY_NAME,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    EMAIL_TIMEOUT,
    USE_TLS,
    EMAIL_SUBJECT,
    HR_REPORT_SUBJECT
)


class EmailService:
    """
    Enterprise Email Service

    Features
    --------
    • Employee Email
    • HR Email
    • Batch Email
    • SMTP Connection Test
    • HTML Email Support
    """

    def __init__(self):

        self.company = COMPANY_NAME

        self.server = SMTP_SERVER

        self.port = SMTP_PORT

        self.username = SMTP_USERNAME

        self.password = SMTP_PASSWORD

        self.timeout = EMAIL_TIMEOUT

        self.use_tls = USE_TLS
        # =====================================================
    # Send Email
    # =====================================================

    def send_email(
        self,
        receiver,
        subject,
        body,
        html=False
    ):

        # ------------------------------------------
        # Validate Email
        # ------------------------------------------

        if not receiver:

            print("Receiver email is empty.")

            return False

        if not self.username or not self.password:

            print("SMTP username/password not configured.")

            return False

        try:

            message = MIMEMultipart()

            message["From"] = f"{self.company} <{self.username}>"

            message["To"] = receiver

            message["Subject"] = subject

            # ------------------------------------------
            # Email Body
            # ------------------------------------------

            if html:

                message.attach(

                    MIMEText(
                        body,
                        "html",
                        "utf-8"
                    )

                )

            else:

                message.attach(

                    MIMEText(
                        body,
                        "plain",
                        "utf-8"
                    )

                )

            # ------------------------------------------
            # SMTP Connection
            # ------------------------------------------

            smtp = smtplib.SMTP(

                self.server,

                self.port,

                timeout=self.timeout

            )

            smtp.ehlo()

            if self.use_tls:

                smtp.starttls()

                smtp.ehlo()

            smtp.login(

                self.username,

                self.password

            )

            smtp.sendmail(

                self.username,

                receiver,

                message.as_string()

            )

            smtp.quit()

            print(f"Email sent successfully to {receiver}")

            return True

        except Exception as error:

            print(f"Email Sending Failed: {error}")

            return False
        # =====================================================
    # Send Batch Emails
    # =====================================================

    def send_batch(
        self,
        employees
    ):

        sent = 0

        failed = 0

        skipped = 0

        total = len(employees)

        for employee in employees:

            receiver = str(

                employee.get(
                    "email",
                    ""
                )

            ).strip()

            # ------------------------------------------
            # Skip if Email Not Available
            # ------------------------------------------

            if receiver == "":

                skipped += 1

                continue

            # ------------------------------------------
            # Subject
            # ------------------------------------------

            subject = EMAIL_SUBJECT

            # ------------------------------------------
            # Body
            # ------------------------------------------

            body = employee.get(

                "notification",

                "Attendance notification."

            )

            # ------------------------------------------
            # Send Email
            # ------------------------------------------

            success = self.send_email(

                receiver,

                subject,

                body,

                html=False

            )

            if success:

                sent += 1

                print(

                    f"✓ Email Sent : {receiver}"

                )

            else:

                failed += 1

                print(

                    f"✗ Email Failed : {receiver}"

                )

        # ------------------------------------------
        # Summary
        # ------------------------------------------

        success_rate = 0

        if (sent + failed) > 0:

            success_rate = round(

                (sent / (sent + failed)) * 100,

                2

            )

        return {

            "total": total,

            "sent": sent,

            "failed": failed,

            "skipped": skipped,

            "success_rate": success_rate

        }
        # =====================================================
    # Test SMTP Connection
    # =====================================================

    def test_connection(self):

        try:

            smtp = smtplib.SMTP(
                self.server,
                self.port,
                timeout=self.timeout
            )

            smtp.ehlo()

            if self.use_tls:

                smtp.starttls()

                smtp.ehlo()

            smtp.login(
                self.username,
                self.password
            )

            smtp.quit()

            print("SMTP Connection Successful.")

            return True

        except Exception as error:

            print(f"SMTP Connection Failed : {error}")

            return False

    # =====================================================
    # Send HR Report
    # =====================================================

    def send_hr_report(
        self,
        hr_email,
        report
    ):

        if not hr_email:

            return False

        return self.send_email(

            receiver=hr_email,

            subject=HR_REPORT_SUBJECT,

            body=report,

            html=False

        )
        # =====================================================
# End of Email Service
# =====================================================