"""
=========================================================
Attendance Notification System Pro
Overtime Manager
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

from datetime import datetime

from services.database_manager import DatabaseManager

from config import (
    SHIFT_END,
    DAILY_OT_LIMIT,
    DAILY_OT_WARNING,
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING
)


class OvertimeManager:

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = DatabaseManager()

        self.shift_end = datetime.strptime(
            SHIFT_END,
            "%H:%M"
        )

    # =====================================================
    # Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(self, minutes):

        if minutes is None or minutes <= 0:
            return "00:00"

        hours = minutes // 60
        mins = minutes % 60

        return f"{hours:02d}:{mins:02d}"

    # =====================================================
    # HH:MM -> Minutes
    # =====================================================

    def time_to_minutes(self, value):

        if value is None:
            return 0

        value = str(value).strip()

        if value in (
            "",
            "-",
            "--",
            "00:00",
            "00:00:00",
            "0",
            "0.0",
            "nan",
            "NaN"
        ):
            return 0

        try:

            hours, minutes = value.split(":")

            return int(hours) * 60 + int(minutes)

        except Exception:

            return 0

    # =====================================================
    # Calculate Daily OT
    # =====================================================

    def calculate_daily_ot(self, out_time):

        if out_time is None:
            return 0

        if not isinstance(out_time, datetime):
            return 0

        overtime = int(
            (out_time - self.shift_end).total_seconds() / 60
        )

        if overtime < 0:
            overtime = 0

        return overtime

    # =====================================================
    # Daily OT Validation
    # =====================================================

    def check_daily_limit(
        self,
        employee,
        overtime_minutes
    ):

        employee["daily_ot_minutes"] = overtime_minutes

        employee["daily_ot"] = self.minutes_to_time(
            overtime_minutes
        )

        if overtime_minutes > DAILY_OT_LIMIT:

            employee["daily_ot_status"] = "Exceeded"

            employee["daily_ot_message"] = (
                "Daily OT exceeded."
            )

        elif overtime_minutes == DAILY_OT_LIMIT:

            employee["daily_ot_status"] = "Limit Reached"

            employee["daily_ot_message"] = (
                "Daily OT limit reached."
            )

        elif overtime_minutes >= DAILY_OT_WARNING:

            employee["daily_ot_status"] = "Warning"

            employee["daily_ot_message"] = (
                "Daily OT nearing limit."
            )

        else:

            employee["daily_ot_status"] = "Normal"

            employee["daily_ot_message"] = (
                "Daily OT within limit."
            )

        return employee

    # =====================================================
    # Monthly OT Validation
    # =====================================================

    def update_monthly_ot(self, employee):

        employee = self.database.update_employee(
            employee
        )

        monthly_minutes = employee.get(
            "monthly_ot_minutes",
            0
        )

        monthly_limit = MONTHLY_OT_LIMIT * 60

        warning_limit = MONTHLY_OT_WARNING * 60

        remaining_minutes = max(
            0,
            monthly_limit - monthly_minutes
        )

        employee["remaining_ot_minutes"] = remaining_minutes

        employee["remaining_ot"] = self.minutes_to_time(
            remaining_minutes
        )

        if monthly_minutes > monthly_limit:

            employee["monthly_status"] = "Exceeded"

            employee["monthly_message"] = (
                "Monthly OT exceeded."
            )

        elif monthly_minutes == monthly_limit:

            employee["monthly_status"] = "Limit Reached"

            employee["monthly_message"] = (
                "Monthly OT limit reached."
            )

        elif monthly_minutes >= warning_limit:

            employee["monthly_status"] = "Warning"

            employee["monthly_message"] = (
                "Monthly OT nearing limit."
            )

        else:

            employee["monthly_status"] = "Normal"

            employee["monthly_message"] = (
                "Monthly OT within limit."
            )

        employee["monthly_ot"] = self.minutes_to_time(
            monthly_minutes
        )

        return employee

    # =====================================================
    # Process Employee Overtime
    # =====================================================

    def process(
        self,
        employee,
        out_time
    ):

        overtime_minutes = self.calculate_daily_ot(
            out_time
        )

        employee = self.check_daily_limit(
            employee,
            overtime_minutes
        )

        employee = self.update_monthly_ot(
            employee
        )

        return employee