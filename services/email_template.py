"""
=========================================================
Attendance Notification System Pro
Email Template
Version : 8.0 Enterprise (Ultra Performance)
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
    """
    Enterprise Email Template Generator

    Features
    --------
    • Employee Attendance Summary
    • Overtime Information
    • Monthly Warning Messages
    • Professional Email Format
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.subject = (

            f"{COMPANY_NAME} - Attendance Notification"

        )

    # =====================================================
    # Generate Email
    # =====================================================

    def generate(

        self,

        employee

    ):

        status = employee.get(

            "status",

            []

        )

        if isinstance(

            status,

            list

        ):

            status_text = ", ".join(status)

            if not status_text:

                status_text = "On Time"

        else:

            status_text = str(status)

        body = f"""
Dear {employee.get('name', 'Employee')},

Greetings from {COMPANY_NAME}.

Your attendance has been processed successfully.

====================================================

EMPLOYEE DETAILS

Employee ID      : {employee.get('employee_id', '')}
Employee Name    : {employee.get('name', '')}
Department       : {employee.get('department', '')}
Designation      : {employee.get('designation', '')}
Attendance Date  : {employee.get('attendance_date', '')}

====================================================

ATTENDANCE DETAILS

Punch In         : {employee.get('punch_in', '--')}
Punch Out        : {employee.get('punch_out', '--')}

Attendance Status : {status_text}

Late Punch        : {employee.get('late_minutes', '00:00')}
Early Punch Out   : {employee.get('early_minutes', '00:00')}

====================================================

OVERTIME DETAILS

Daily OT          : {employee.get('daily_ot', '00:00')}
Daily OT Status   : {employee.get('daily_status', 'Normal')}

Monthly OT        : {employee.get('monthly_ot', '00:00')}
Monthly Status    : {employee.get('monthly_status', 'Normal')}

Remaining OT      : {employee.get('remaining_ot', '00:00')}

====================================================

NOTIFICATION

{employee.get('notification', 'Attendance processed successfully.')}

====================================================

COMPANY POLICY

Shift Timing      : {SHIFT_START} - {SHIFT_END}

Daily OT Limit    : {DAILY_OT_LIMIT} Minutes

Monthly OT Limit  : {MONTHLY_OT_LIMIT} Hours
"""
# =====================================================
        # Monthly Warning
        # =====================================================

        monthly_status = employee.get(

            "monthly_status",

            "Normal"

        )

        if monthly_status == "Warning":

            body += """

====================================================

⚠ MONTHLY OT WARNING

Your monthly overtime is approaching the company limit.

Please coordinate with your Reporting Manager.

"""

        elif monthly_status == "Limit Reached":

            body += """

====================================================

🚨 MONTHLY OT LIMIT REACHED

You have reached the maximum monthly overtime limit.

Further overtime requires HR approval.

"""

        elif monthly_status == "Exceeded":

            body += """

====================================================

❌ MONTHLY OT EXCEEDED

Your monthly overtime has exceeded the company limit.

Please contact the HR Department immediately.

"""

        else:

            body += """

====================================================

✅ MONTHLY OT STATUS

Your monthly overtime is within the permitted limit.

"""

        # =====================================================
        # Footer
        # =====================================================

        body += f"""

====================================================

Regards,

{HR_NAME}

{COMPANY_NAME}

This is an automatically generated email.

Please do not reply to this email.

====================================================
"""

        return (

            self.subject,

            body

        )
        