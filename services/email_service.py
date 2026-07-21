"""
=========================================================
Attendance Notification System Pro
Email Service
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    COMPANY_NAME,
    MONTHLY_OT_LIMIT
)


class EmailService:

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.sender = EMAIL_ADDRESS
        self.password = EMAIL_PASSWORD
        self.server = SMTP_SERVER
        self.port = SMTP_PORT

    # =====================================================
    # Generate Email Message
    # =====================================================

    def generate_message(self, employee):

        remaining = (
            MONTHLY_OT_LIMIT * 60
        ) - employee.get(
            "monthly_ot_minutes",
            0
        )

        if remaining < 0:
            remaining = 0

        remaining_ot = (
            f"{remaining//60:02d}:{remaining%60:02d}"
        )

        body = f"""
Dear {employee['name']},

Attendance Notification

Employee ID : {employee['employee_id']}
Department  : {employee['department']}
Designation : {employee['designation']}

Attendance Date : {employee['attendance_date']}

Punch In  : {employee['punch_in']}
Punch Out : {employee['punch_out']}

Daily Overtime     : {employee['daily_ot']}
Monthly Overtime   : {employee['monthly_ot']}
Remaining OT Limit : {remaining_ot}

Daily Status   : {employee['daily_ot_status']}
Monthly Status : {employee['monthly_status']}

-------------------------------------------------

{employee['notification']}

-------------------------------------------------

Regards,

HR Department

{COMPANY_NAME}
"""

        return body

    # =====================================================
    # Send Email
    # =====================================================

    def send_email(self, employee):

        email = employee.get(
            "email",
            ""
        ).strip()

        if not email:
            return False

        try:

            message = MIMEMultipart()

            message["From"] = self.sender
            message["To"] = email
            message["Subject"] = (
                f"Attendance Notification - "
                f"{employee['attendance_date']}"
            )

            message.attach(
                MIMEText(
                    self.generate_message(employee),
                    "plain"
                )
            )

            server = smtplib.SMTP(
                self.server,
                self.port
            )

            server.starttls()

            server.login(
                self.sender,
                self.password
            )

            server.sendmail(
                self.sender,
                email,
                message.as_string()
            )

            server.quit()

            return True

        except Exception as e:

            print(f"Email Error ({email}) : {e}")

            return False