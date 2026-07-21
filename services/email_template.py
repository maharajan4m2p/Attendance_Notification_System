"""
=========================================================
Attendance Notification System Pro
Email Template
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

from config import (
    COMPANY_NAME,
    HR_NAME,
    SHIFT_START,
    SHIFT_END,
    DAILY_OT_LIMIT,
    MONTHLY_OT_LIMIT
)


class EmailTemplate:

    def __init__(self):
        pass

    # =====================================================
    # Generate Email
    # =====================================================

    def generate(self, employee):

        subject = f"{COMPANY_NAME} - Attendance Notification"

        status = employee.get("status", [])

        if isinstance(status, list):
            status_text = ", ".join(status)
        else:
            status_text = str(status)

        body = f"""
Dear {employee.get("name", "Employee")},

Greetings from {COMPANY_NAME}.

Your attendance has been processed successfully.

====================================================

EMPLOYEE DETAILS

Employee ID      : {employee.get("employee_id", "")}
Employee Name    : {employee.get("name", "")}
Department       : {employee.get("department", "")}
Designation      : {employee.get("designation", "")}
Attendance Date  : {employee.get("attendance_date", "")}

====================================================

ATTENDANCE DETAILS

Punch In         : {employee.get("punch_in", "--")}
Punch Out        : {employee.get("punch_out", "--")}

Status           : {status_text}

Late Punch       : {employee.get("late_minutes", "00:00")}
Early Punch Out  : {employee.get("early_minutes", "00:00")}

====================================================

OVERTIME DETAILS

Daily OT         : {employee.get("daily_ot", "00:00")}
Daily OT Status  : {employee.get("daily_ot_status", "Allowed")}

Monthly OT       : {employee.get("monthly_ot", "00:00")}
Monthly Status   : {employee.get("monthly_status", "Allowed")}

====================================================

NOTIFICATION

{employee.get("notification", "Attendance processed successfully.")}

====================================================

COMPANY POLICY

Shift Timing      : {SHIFT_START} - {SHIFT_END}

Daily OT Limit    : {DAILY_OT_LIMIT} Minutes

Monthly OT Limit  : {MONTHLY_OT_LIMIT} Hours
"""

        # ==============================================
        # Monthly Warning
        # ==============================================

        if employee.get("monthly_status") == "Warning":

            body += """

====================================================

⚠ WARNING

Your monthly overtime is approaching the company limit.

Please coordinate with your Reporting Manager.

"""

        # ==============================================
        # Monthly Exceeded
        # ==============================================

        elif employee.get("monthly_status") == "Exceeded":

            body += """

====================================================

🚨 ALERT

Your monthly overtime has exceeded the company limit.

Please contact the HR Department immediately.

"""

        # ==============================================
        # Footer
        # ==============================================

        body += f"""

====================================================

Regards,

{HR_NAME}

{COMPANY_NAME}

This is an automatically generated email.

Please do not reply to this email.

====================================================
"""

        return subject, body