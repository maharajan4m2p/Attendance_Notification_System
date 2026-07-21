"""
=========================================================
Attendance Notification System Pro
Overtime Manager
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""

from datetime import datetime

from config import (
    SHIFT_END,
    DAILY_OT_LIMIT,
    DAILY_OT_WARNING,
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING
)

from services.database_manager import DatabaseManager


class OvertimeManager:
    """
    Enterprise Overtime Processing Engine

    Features
    --------
    • Daily OT calculation
    • Monthly OT tracking
    • Shared DatabaseManager
    • Enterprise performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(
        self,
        database=None
    ):

        self.database = database or DatabaseManager()

        self.shift_end = datetime.strptime(
            SHIFT_END,
            "%H:%M"
        )

        self.empty_time_values = {

            "",

            "-",

            "--",

            "00:00",

            "00:00:00",

            "0",

            "0.0",

            "nan",

            "NaN",

            "None"

        }

    # =====================================================
    # Convert Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(
        self,
        minutes
    ):

        if minutes is None or minutes <= 0:

            return "00:00"

        hours = int(minutes // 60)

        mins = int(minutes % 60)

        return f"{hours:02d}:{mins:02d}"

    # =====================================================
    # Convert HH:MM -> Minutes
    # =====================================================

    def time_to_minutes(
        self,
        value
    ):

        if value is None:

            return 0

        value = str(value).strip()

        if value in self.empty_time_values:

            return 0

        try:

            hours, minutes = value.split(":")

            return (

                int(hours) * 60

                +

                int(minutes)

            )

        except Exception:

            return 0

    # =====================================================
    # Calculate Daily Overtime
    # =====================================================

    def calculate_daily_ot(
        self,
        out_time
    ):

        if out_time is None:

            return 0

        if not isinstance(
            out_time,
            datetime
        ):

            return 0

        overtime = int(

            (
                out_time -

                self.shift_end

            ).total_seconds() // 60

        )

        return max(
            0,
            overtime
        )
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

        # -----------------------------------------
        # Daily Status
        # -----------------------------------------

        if overtime_minutes > DAILY_OT_LIMIT:

            status = "Exceeded"
            message = "Daily OT exceeded."

        elif overtime_minutes == DAILY_OT_LIMIT:

            status = "Limit Reached"
            message = "Daily OT limit reached."

        elif overtime_minutes >= DAILY_OT_WARNING:

            status = "Warning"
            message = "Daily OT nearing limit."

        else:

            status = "Normal"
            message = "Daily OT within limit."

        employee["daily_status"] = status
        employee["daily_message"] = message

        return employee

    # =====================================================
    # Monthly OT Validation
    # =====================================================

    def update_monthly_ot(
        self,
        employee
    ):

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

        employee["monthly_ot"] = self.minutes_to_time(
            monthly_minutes
        )

        employee["remaining_ot"] = self.minutes_to_time(
            remaining_minutes
        )

        employee["monthly_ot_minutes"] = monthly_minutes
        employee["remaining_ot_minutes"] = remaining_minutes

        # -----------------------------------------
        # Monthly Status
        # -----------------------------------------

        if monthly_minutes > monthly_limit:

            status = "Exceeded"
            message = "Monthly OT exceeded."

        elif monthly_minutes == monthly_limit:

            status = "Limit Reached"
            message = "Monthly OT limit reached."

        elif monthly_minutes >= warning_limit:

            status = "Warning"
            message = "Monthly OT nearing limit."

        else:

            status = "Normal"
            message = "Monthly OT within limit."

        employee["monthly_status"] = status
        employee["monthly_message"] = message

        employee["warning"] = (
            status == "Warning"
        )

        employee["limit_reached"] = (
            status == "Limit Reached"
        )

        employee["ot_exceeded"] = (
            status == "Exceeded"
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