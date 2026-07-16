"""
=========================================================
Email Template
Developed by Maharajan
=========================================================
"""

from config import COMPANY_NAME, HR_NAME


class EmailTemplate:

    def generate(self, employee):

        subject = "Attendance Notification"

        body = f"""
Dear {employee['name']},

Greetings from {COMPANY_NAME}.

This is your attendance notification for today.

========================================

Employee ID : {employee['employee_id']}

Employee Name : {employee['name']}

Punch In : {employee['punch_in']}

Punch Out : {employee['punch_out']}

Status

{chr(10).join(employee['status'])}

========================================

{employee['notification']}

If you believe this attendance information is incorrect,
please contact the HR Department.

Regards,

{HR_NAME}

{COMPANY_NAME}
"""

        return subject, body