"""
=========================================================
Attendance Notification System Pro
Enterprise Notification Service
Version : 14.0 Enterprise
=========================================================
"""

from datetime import datetime
from typing import Any
from config import (
    COMPANY_NAME,
    MONTHLY_OT_LIMIT_HOURS,
    MONTHLY_OT_WARNING_HOURS,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)


class NotificationService:
    """
    Enterprise Notification Service

    Generates

        • Employee Notification
        • HR Notification
        • WhatsApp Notification
        • Monthly Warning
        • Monthly Limit Reached
        • Monthly Exceeded
        • Notification Summary
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.company = COMPANY_NAME

        self.monthly_limit = MONTHLY_OT_LIMIT_HOURS

        self.warning_limit = MONTHLY_OT_WARNING_HOURS

        self.generated_time = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        self.separator = "=" * 80

    # =====================================================
    # Helper
    # =====================================================

    def get_value(
        self,
        employee,
        key,
        default=""
    ):

        value = employee.get(
            key,
            default
        )

        if value is None:

            return default

        return value
    

    # =====================================================
    # Generate Employee Notification
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

        message.append(
            f"Generated On : {self.generated_time}"
        )

        message.append("")

        # =====================================================
        # Employee Details
        # =====================================================

        message.append(
            f"Employee ID      : {self.get_value(employee,'employee_id')}"
        )

        message.append(
            f"Employee Name    : {self.get_value(employee,'name')}"
        )

        message.append(
            f"Department       : {self.get_value(employee,'department')}"
        )

        message.append(
            f"Designation      : {self.get_value(employee,'designation')}"
        )

        message.append("")

        # =====================================================
        # Attendance Details
        # =====================================================

        message.append(
            f"Attendance Date  : {self.get_value(employee,'attendance_date')}"
        )

        message.append(
            f"Punch In         : {self.get_value(employee,'punch_in','--')}"
        )

        message.append(
            f"Punch Out        : {self.get_value(employee,'punch_out','--')}"
        )

        message.append("")

        # =====================================================
        # Overtime Details
        # =====================================================

        message.append(
            f"Daily OT         : {self.get_value(employee,'daily_ot','00:00')}"
        )

        message.append(
            f"Monthly OT       : {self.get_value(employee,'monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT     : {self.get_value(employee,'remaining_ot','25:00')}"
        )

        message.append(
            f"Monthly Status   : {self.get_value(employee,'monthly_status',NORMAL_STATUS)}"
        )

        message.append("")

        # =====================================================
        # Attendance Remarks
        # =====================================================

        message.append("Attendance Status")

        status_list = employee.get(
            "status",
            []
        )

        if status_list:

            for status in status_list:

                message.append(
                    f"• {status}"
                )

        else:

            message.append(
                "• On Time"
            )

        message.append("")

        # =====================================================
        # Monthly OT Notification
        # =====================================================

        monthly_status = employee.get(
            "monthly_status",
            NORMAL_STATUS
        )

        if monthly_status == WARNING_STATUS:

            message.append(
                f"⚠ Warning: Your monthly overtime is approaching the {self.warning_limit} hour limit."
            )

        elif monthly_status == LIMIT_REACHED_STATUS:

            message.append(
                f"⚠ You have reached the monthly overtime limit ({self.monthly_limit} Hours)."
            )

        elif monthly_status == EXCEEDED_STATUS:

            message.append(
                "🚨 Monthly overtime limit exceeded."
            )

            message.append(
                "Please contact the HR department immediately."
            )

        else:

            message.append(
                "✅ Attendance processed successfully."
            )

        message.append("")
        message.append("Thank You")
        message.append(self.company)

        return "\n".join(message)
    
    # =====================================================
    # Generate Notification Summary
# =====================================================

    def generate_summary(self, employees, summary):

        lines = []

        lines.append(self.separator)
        lines.append(self.company)
        lines.append("ATTENDANCE SUMMARY")
        lines.append(self.separator)

        lines.append(f"Total Employees : {summary.get('total', 0)}")
        lines.append(f"Present         : {summary.get('present', 0)}")
        lines.append(f"Absent          : {summary.get('absent', 0)}")
        lines.append(f"Late Punch      : {summary.get('late_in', 0)}")
        lines.append(f"Early Out       : {summary.get('early_out', 0)}")
        lines.append(f"Missing In      : {summary.get('missing_in', 0)}")
        lines.append(f"Missing Out     : {summary.get('missing_out', 0)}")
        lines.append(f"Employees OT    : {summary.get('overtime', 0)}")

        lines.append(self.separator)

        return "\n".join(lines)
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

        message.append(
            f"Generated On : {self.generated_time}"
        )

        message.append("")

        message.append(
            f"Dear {self.get_value(employee,'name','Employee')},"
        )

        message.append("")

        message.append(
            "Your monthly overtime is approaching the permitted limit."
        )

        message.append("")

        message.append(
            f"Monthly OT       : {self.get_value(employee,'monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT     : {self.get_value(employee,'remaining_ot','00:00')}"
        )

        message.append(
            f"Monthly Status   : {self.get_value(employee,'monthly_status',WARNING_STATUS)}"
        )

        message.append("")

        message.append(
            f"Warning Limit    : {self.warning_limit} Hours"
        )

        message.append(
            f"Monthly Limit    : {self.monthly_limit} Hours"
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

        message.append(
            f"Generated On : {self.generated_time}"
        )

        message.append("")

        message.append(
            f"Dear {self.get_value(employee,'name','Employee')},"
        )

        message.append("")

        message.append(
            "You have reached the monthly overtime limit."
        )

        message.append("")

        message.append(
            f"Monthly OT       : {self.get_value(employee,'monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT     : {self.get_value(employee,'remaining_ot','00:00')}"
        )

        message.append(
            f"Monthly Status   : {self.get_value(employee,'monthly_status',LIMIT_REACHED_STATUS)}"
        )

        message.append("")

        message.append(
            "Further overtime requires HR approval."
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

        message.append(
            f"Generated On : {self.generated_time}"
        )

        message.append("")

        message.append(
            f"Dear {self.get_value(employee,'name','Employee')},"
        )

        message.append("")

        message.append(
            "Your monthly overtime has exceeded the approved limit."
        )

        message.append("")

        message.append(
            f"Monthly OT       : {self.get_value(employee,'monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT     : {self.get_value(employee,'remaining_ot','00:00')}"
        )

        message.append(
            f"Monthly Status   : {self.get_value(employee,'monthly_status',EXCEEDED_STATUS)}"
        )

        message.append("")

        message.append(
            "Please contact the HR department immediately."
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
        message.append("HR ATTENDANCE NOTIFICATION")
        message.append(self.separator)

        message.append(
            f"Generated On : {self.generated_time}"
        )

        message.append("")

        message.append(
            f"Employee ID      : {self.get_value(employee,'employee_id')}"
        )

        message.append(
            f"Employee Name    : {self.get_value(employee,'name')}"
        )

        message.append(
            f"Department       : {self.get_value(employee,'department')}"
        )

        message.append(
            f"Designation      : {self.get_value(employee,'designation')}"
        )

        message.append("")

        message.append(
            f"Attendance Date  : {self.get_value(employee,'attendance_date')}"
        )

        message.append(
            f"Punch In         : {self.get_value(employee,'punch_in','--')}"
        )

        message.append(
            f"Punch Out        : {self.get_value(employee,'punch_out','--')}"
        )

        message.append("")

        message.append(
            f"Daily OT         : {self.get_value(employee,'daily_ot','00:00')}"
        )

        message.append(
            f"Monthly OT       : {self.get_value(employee,'monthly_ot','00:00')}"
        )

        message.append(
            f"Remaining OT     : {self.get_value(employee,'remaining_ot','25:00')}"
        )

        message.append(
            f"Monthly Status   : {self.get_value(employee,'monthly_status',NORMAL_STATUS)}"
        )

        message.append("")

        status_list = employee.get(
            "status",
            []
        )

        if status_list:

            message.append("Attendance Remarks")

            for status in status_list:

                message.append(
                    f"• {status}"
                )

        else:

            message.append("Attendance Remarks")
            message.append("• On Time")

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
            f"👤 {self.get_value(employee,'name')}"
        )

        message.append(
            f"🆔 {self.get_value(employee,'employee_id')}"
        )

        message.append("")

        message.append(
            f"📅 {self.get_value(employee,'attendance_date')}"
        )

        message.append(
            f"🕘 IN : {self.get_value(employee,'punch_in','--')}"
        )

        message.append(
            f"🕠 OUT : {self.get_value(employee,'punch_out','--')}"
        )

        message.append("")

        message.append(
            f"🕒 Daily OT : {self.get_value(employee,'daily_ot','00:00')}"
        )

        message.append(
            f"📅 Monthly OT : {self.get_value(employee,'monthly_ot','00:00')}"
        )

        message.append(
            f"⏳ Remaining OT : {self.get_value(employee,'remaining_ot','25:00')}"
        )

        message.append(
            f"📊 Status : {self.get_value(employee,'monthly_status',NORMAL_STATUS)}"
        )

        message.append("")

        status_list = employee.get(
            "status",
            []
        )

        if status_list:

            message.append("Status")

            for status in status_list:

                message.append(
                    f"• {status}"
                )

        else:

            message.append("Status")
            message.append("• On Time")

        message.append("")
        message.append("Thank You")
        message.append(self.company)

        return "\n".join(message)
    # =====================================================
    # Notification Summary
    # =====================================================

    def notification_summary(
        self,
        employees
    ): 

        summary: dict[str, Any] = {

            "total": len(employees),

            "normal": 0,

            "warning": 0,

            "limit_reached": 0,

            "exceeded": 0,

            "late": 0,

            "early": 0,

            "missing": 0,

            "overtime": 0,

            "total_monthly_ot_minutes": 0,

            "total_remaining_ot_minutes": 0,

            "total_monthly_ot": "",

            "total_remaining_ot": ""

        }

        for employee in employees:

            monthly_status = employee.get(
                "monthly_status",
                NORMAL_STATUS
            )

            if monthly_status == NORMAL_STATUS:

                summary["normal"] += 1

            elif monthly_status == WARNING_STATUS:

                summary["warning"] += 1

            elif monthly_status == LIMIT_REACHED_STATUS:

                summary["limit_reached"] += 1

            elif monthly_status == EXCEEDED_STATUS:

                summary["exceeded"] += 1

            summary["total_monthly_ot_minutes"] += int(

                employee.get(
                    "monthly_ot_minutes",
                    0
                )

            )

            summary["total_remaining_ot_minutes"] += int(

                employee.get(
                    "remaining_ot_minutes",
                    0
                )

            )

            for status in employee.get(
                "status",
                []
            ):

                if "Late Punch" in status:

                    summary["late"] += 1

                elif "Early Out" in status:

                    summary["early"] += 1

                elif "Missing Punch" in status:

                    summary["missing"] += 1

                elif "Daily OT" in status:

                    summary["overtime"] += 1

        monthly_hours = summary[
            "total_monthly_ot_minutes"
        ] // 60

        monthly_minutes = summary[
            "total_monthly_ot_minutes"
        ] % 60

        remaining_hours = summary[
            "total_remaining_ot_minutes"
        ] // 60

        remaining_minutes = summary[
            "total_remaining_ot_minutes"
        ] % 60

        summary["total_monthly_ot"] = (

            f"{monthly_hours:02d}:{monthly_minutes:02d}"

        )

        summary["total_remaining_ot"] = (

            f"{remaining_hours:02d}:{remaining_minutes:02d}"

        )

        return summary


# =====================================================
# End of Notification Service
# =====================================================