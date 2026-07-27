"""
=========================================================
Attendance Notification System Pro
Enterprise Notification Service
Version : 13.0 Enterprise
=========================================================
"""

from datetime import datetime

from config import (
    COMPANY_NAME,
    MONTHLY_OT_LIMIT_HOURS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)


class NotificationService:
    """
    Enterprise Notification Service

    Generates:
        • Employee Notification
        • HR Notification
        • WhatsApp Notification
        • Monthly OT Warning
        • Monthly OT Limit
        • Monthly OT Exceeded
    """

    def __init__(self):

        self.company = COMPANY_NAME

        self.monthly_limit = MONTHLY_OT_LIMIT_HOURS

        self.generated_time = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        self.separator = "=" * 60
        # =====================================================
    # Employee Notification
    # =====================================================

    def generate_message(
        self,
        employee
    ):

        message = []

        message.append(self.separator)
        message.append(self.company)
        message.append("EMPLOYEE ATTENDANCE NOTIFICATION")
        message.append(self.separator)
        message.append(f"Generated On : {self.generated_time}")
        message.append("")

        # ------------------------------------------
        # Employee Details
        # ------------------------------------------

        message.append(
            f"Employee ID      : {employee.get('employee_id', '')}"
        )

        message.append(
            f"Employee Name    : {employee.get('name', '')}"
        )

        message.append(
            f"Department       : {employee.get('department', '')}"
        )

        message.append(
            f"Designation      : {employee.get('designation', '')}"
        )

        message.append("")

        # ------------------------------------------
        # Attendance Details
        # ------------------------------------------

        message.append(
            f"Attendance Date  : {employee.get('attendance_date', '')}"
        )

        message.append(
            f"Punch In         : {employee.get('punch_in', '--')}"
        )

        message.append(
            f"Punch Out        : {employee.get('punch_out', '--')}"
        )

        message.append("")

        # ------------------------------------------
        # Attendance Status
        # ------------------------------------------

        message.append("Attendance Status")

        for status in employee.get("status", []):

            message.append(
                f"• {status}"
            )

        if len(employee.get("status", [])) == 0:

            message.append("• On Time")

        message.append("")

        # ------------------------------------------
        # Overtime Details
        # ------------------------------------------

        message.append(
            f"Daily OT         : {employee.get('daily_ot', '00:00')}"
        )

        message.append(
            f"Monthly OT       : {employee.get('monthly_ot', '00:00')}"
        )

        message.append(
            f"Remaining OT     : {employee.get('remaining_ot', '25:00')}"
        )

        message.append(
            f"Monthly Status   : {employee.get('monthly_status', 'Normal')}"
        )

        message.append("")

        # ------------------------------------------
        # Notification
        # ------------------------------------------

        monthly_status = employee.get(
            "monthly_status",
            ""
        )

        if monthly_status == WARNING_STATUS:

            message.append(
                "⚠ Monthly overtime is approaching the allowed limit."
            )

        elif monthly_status == LIMIT_REACHED_STATUS:

            message.append(
                "⚠ Monthly overtime limit has been reached."
            )

        elif monthly_status == EXCEEDED_STATUS:

            message.append(
                "🚨 Monthly overtime limit has been exceeded. Please contact HR."
            )

        else:

            message.append(
                "✓ Attendance processed successfully."
            )

        message.append("")
        message.append("Thank you.")
        message.append(self.company)

        return "\n".join(message)
    # =====================================================
    # Monthly OT Warning
    # =====================================================

    def monthly_warning_message(
        self,
        employee
    ):

        message = []

        message.append(self.separator)
        message.append(self.company)
        message.append("MONTHLY OVERTIME WARNING")
        message.append(self.separator)
        message.append("")

        message.append(
            f"Dear {employee.get('name','Employee')},"
        )

        message.append("")

        message.append(
            "Your monthly overtime is approaching the allowed limit."
        )

        message.append("")

        message.append(
            f"Monthly OT     : {employee.get('monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT   : {employee.get('remaining_ot','00:00')}"
        )

        message.append(
            f"Status         : {employee.get('monthly_status','Normal')}"
        )

        message.append("")

        message.append(
            "Please plan your working hours accordingly."
        )

        message.append("")
        message.append("Thank You")
        message.append(self.company)

        return "\n".join(message)

    # =====================================================
    # Monthly OT Limit Reached
    # =====================================================

    def limit_reached_message(
        self,
        employee
    ):

        message = []

        message.append(self.separator)
        message.append(self.company)
        message.append("MONTHLY OVERTIME LIMIT REACHED")
        message.append(self.separator)
        message.append("")

        message.append(
            f"Dear {employee.get('name','Employee')},"
        )

        message.append("")

        message.append(
            "You have reached the monthly overtime limit."
        )

        message.append("")

        message.append(
            f"Monthly OT     : {employee.get('monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT   : {employee.get('remaining_ot','00:00')}"
        )

        message.append(
            f"Status         : {employee.get('monthly_status','Normal')}"
        )

        message.append("")

        message.append(
            "Please contact HR if additional overtime is required."
        )

        message.append("")
        message.append("Thank You")
        message.append(self.company)

        return "\n".join(message)

    # =====================================================
    # Monthly OT Exceeded
    # =====================================================

    def exceeded_message(
        self,
        employee
    ):

        message = []

        message.append(self.separator)
        message.append(self.company)
        message.append("MONTHLY OVERTIME EXCEEDED")
        message.append(self.separator)
        message.append("")

        message.append(
            f"Dear {employee.get('name','Employee')},"
        )

        message.append("")

        message.append(
            "Your monthly overtime has exceeded the allowed limit."
        )

        message.append("")

        message.append(
            f"Monthly OT     : {employee.get('monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT   : {employee.get('remaining_ot','00:00')}"
        )

        message.append(
            f"Status         : {employee.get('monthly_status','Exceeded')}"
        )

        message.append("")

        message.append(
            "Please contact your HR department immediately."
        )

        message.append("")
        message.append("Thank You")
        message.append(self.company)

        return "\n".join(message)
    # =====================================================
    # HR Notification
    # =====================================================

    def hr_notification(
        self,
        employee
    ):

        message = []

        message.append(self.separator)
        message.append(self.company)
        message.append("HR NOTIFICATION")
        message.append(self.separator)

        message.append(
            f"Employee ID      : {employee.get('employee_id','')}"
        )

        message.append(
            f"Employee Name    : {employee.get('name','')}"
        )

        message.append(
            f"Department       : {employee.get('department','')}"
        )

        message.append(
            f"Designation      : {employee.get('designation','')}"
        )

        message.append("")

        message.append(
            f"Attendance Date  : {employee.get('attendance_date','')}"
        )

        message.append(
            f"Punch In         : {employee.get('punch_in','--')}"
        )

        message.append(
            f"Punch Out        : {employee.get('punch_out','--')}"
        )

        message.append("")

        message.append(
            f"Daily OT         : {employee.get('daily_ot','00:00')}"
        )

        message.append(
            f"Monthly OT       : {employee.get('monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT     : {employee.get('remaining_ot','25:00')}"
        )

        message.append(
            f"Monthly Status   : {employee.get('monthly_status','Normal')}"
        )

        message.append("")

        if employee.get("status"):

            message.append("Attendance Remarks")

            for status in employee["status"]:

                message.append(
                    f"• {status}"
                )

        return "\n".join(message)

    # =====================================================
    # WhatsApp Message
    # =====================================================

    def whatsapp_message(
        self,
        employee
    ):

        message = []

        message.append(f"🏢 {self.company}")
        message.append("")
        message.append(
            f"👤 {employee.get('name','')}"
        )

        message.append(
            f"🆔 {employee.get('employee_id','')}"
        )

        message.append("")

        message.append(
            f"🕘 IN : {employee.get('punch_in','--')}"
        )

        message.append(
            f"🕕 OUT : {employee.get('punch_out','--')}"
        )

        message.append("")

        message.append(
            f"🕒 Daily OT : {employee.get('daily_ot','00:00')}"
        )

        message.append(
            f"📅 Monthly OT : {employee.get('monthly_ot','00:00')}"
        )

        message.append(
            f"⏳ Remaining : {employee.get('remaining_ot','25:00')}"
        )

        message.append("")

        if employee.get("status"):

            message.append("Status")

            for status in employee["status"]:

                message.append(f"• {status}")

        message.append("")
        message.append("Thank You")

        return "\n".join(message)

    # =====================================================
    # Notification Summary
    # =====================================================

    def notification_summary(
        self,
        employees
    ):

        summary = {

            "total": len(employees),

            "warning": 0,

            "limit_reached": 0,

            "exceeded": 0,

            "late": 0,

            "early": 0,

            "missing": 0,

            "overtime": 0

        }

        for employee in employees:

            monthly_status = employee.get(
                "monthly_status",
                ""
            )

            if monthly_status == WARNING_STATUS:
                summary["warning"] += 1

            elif monthly_status == LIMIT_REACHED_STATUS:
                summary["limit_reached"] += 1

            elif monthly_status == EXCEEDED_STATUS:
                summary["exceeded"] += 1

            for status in employee.get("status", []):

                if "Late Punch" in status:
                    summary["late"] += 1

                elif "Early Out" in status:
                    summary["early"] += 1

                elif "Missing Punch" in status:
                    summary["missing"] += 1

                elif "Daily OT" in status:
                    summary["overtime"] += 1

        return summary


# =====================================================
# End of Notification Service
# =====================================================