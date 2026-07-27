"""
=========================================================
Attendance Notification System Pro
Enterprise Email Template
Version : 13.0 Enterprise
=========================================================
"""

from datetime import datetime

from config import (
    COMPANY_NAME,
    SHIFT_START,
    SHIFT_END,
    DAILY_OT_LIMIT,
    MONTHLY_OT_LIMIT_HOURS,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS,
)


class EmailTemplate:
    """
    Enterprise Email Template Generator

    Features
    --------
    ✓ Employee Attendance Summary
    ✓ Daily Attendance Status
    ✓ Monthly OT Status
    ✓ Company Policy
    ✓ Professional Email Format
    ✓ HTML Email Support
    """

    def __init__(self):

        self.company = COMPANY_NAME

        self.subject = (
            f"{COMPANY_NAME} - Attendance Notification"
        )

        self.generated_on = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )
        # =====================================================
    # Generate Email
    # =====================================================

    def generate(self, employee):

        status = employee.get("status", [])

        if isinstance(status, list):

            status_text = ", ".join(status)

            if not status_text:

                status_text = "On Time"

        else:

            status_text = str(status)

        body = f"""
Dear {employee.get('name', 'Employee')},

Greetings from {self.company}.

Your attendance has been processed successfully.

====================================================

EMPLOYEE DETAILS

Employee ID        : {employee.get('employee_id', '')}

Employee Name      : {employee.get('name', '')}

Department         : {employee.get('department', '')}

Designation        : {employee.get('designation', '')}

Attendance Date    : {employee.get('attendance_date', '')}

====================================================

ATTENDANCE DETAILS

Punch In           : {employee.get('punch_in', '--')}

Punch Out          : {employee.get('punch_out', '--')}

Attendance Status  : {status_text}

Late Minutes       : {employee.get('late_minutes', '00:00')}

Early Out Minutes  : {employee.get('early_minutes', '00:00')}

====================================================

OVERTIME DETAILS

Daily OT           : {employee.get('daily_ot', '00:00')}

Daily Status       : {employee.get('daily_status', NORMAL_STATUS)}

Monthly OT         : {employee.get('monthly_ot', '00:00')}

Monthly Status     : {employee.get('monthly_status', NORMAL_STATUS)}

Remaining OT       : {employee.get('remaining_ot', '00:00')}

====================================================

ATTENDANCE NOTIFICATION

{employee.get('notification', 'Attendance processed successfully.')}

====================================================

COMPANY POLICY

Shift Timing       : {SHIFT_START} - {SHIFT_END}

Daily OT Limit     : {DAILY_OT_LIMIT} Minutes

Monthly OT Limit   : {MONTHLY_OT_LIMIT_HOURS} Hours
"""
# =====================================================
        # Monthly OT Status
        # =====================================================

        monthly_status = employee.get(
            "monthly_status",
            NORMAL_STATUS
        )

        if monthly_status == WARNING_STATUS:

            body += """

====================================================

⚠️ MONTHLY OT WARNING

Your monthly overtime has crossed the company warning limit.

Please monitor your overtime carefully.

Contact your Reporting Manager if additional overtime is required.

"""

        elif monthly_status == LIMIT_REACHED_STATUS:

            body += """

====================================================

🟠 MONTHLY OT LIMIT REACHED

You have reached the maximum monthly overtime limit.

Any additional overtime requires prior approval from the HR Department.

"""

        elif monthly_status == EXCEEDED_STATUS:

            body += """

====================================================

🔴 MONTHLY OT EXCEEDED

Your monthly overtime has exceeded the company limit.

Please contact the HR Department immediately.

"""

        else:

            body += """

====================================================

✅ MONTHLY OT STATUS

Your monthly overtime is within the permitted company limit.

Keep maintaining your attendance.

"""

        # =====================================================
        # Footer
        # =====================================================

        body += f"""

====================================================

If you have any questions regarding your attendance,
please contact your Reporting Manager or the HR Department.

Generated On : {self.generated_on}

Regards,

HR Department

{self.company}

----------------------------------------------------

This is an automatically generated email from

Attendance Notification System Pro.

Please do not reply to this email.

====================================================
"""

        return (
            self.subject,
            body
        )