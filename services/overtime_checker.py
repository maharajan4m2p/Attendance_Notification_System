"""
=========================================================
Attendance Notification System Pro
Overtime Manager
Version : 10.0 Enterprise
Developed by Maharajan
=========================================================
"""

from datetime import datetime

from config import (
    SHIFT_END,
    DAILY_OT_LIMIT,
    DAILY_OT_WARNING,
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)

from services.database_manager import DatabaseManager


class OvertimeManager:
    """
    Enterprise Overtime Processing Engine

    Features
    --------
    • Daily OT Calculation
    • Monthly OT Tracking
    • Remaining OT Calculation
    • Daily Status
    • Monthly Status
    • Database Synchronization
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self, database=None):

        self.database = database or DatabaseManager()

        self.shift_end = datetime.strptime(
            SHIFT_END,
            "%H:%M"
        )

        self.daily_warning = DAILY_OT_WARNING

        self.daily_limit = DAILY_OT_LIMIT

        self.monthly_warning = MONTHLY_OT_WARNING * 60

        self.monthly_limit = MONTHLY_OT_LIMIT * 60

        self.empty_time_values = {

            "",

            "-",

            "--",

            "0",

            "0.0",

            "00:00",

            "00:00:00",

            "nan",

            "NaN",

            "None",

            "N/A"

        }
        # =====================================================
    # Convert Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(
        self,
        minutes
    ):

        try:

            minutes = int(minutes)

        except (TypeError, ValueError):

            return "00:00"

        if minutes <= 0:

            return "00:00"

        hours = minutes // 60

        mins = minutes % 60

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

        # -----------------------------------------
        # HH:MM Format
        # -----------------------------------------

        if ":" in value:

            try:

                hours, minutes = value.split(":")

                return (

                    int(hours) * 60

                    +

                    int(minutes)

                )

            except Exception:

                return 0

        # -----------------------------------------
        # Numeric Format
        # -----------------------------------------

        try:

            return int(float(value))

        except Exception:

            return 0
        # =====================================================
    # Calculate Daily Overtime
    # =====================================================

    def calculate_daily_ot(
        self,
        out_time
    ):

        # -----------------------------------------
        # Invalid Punch Out
        # -----------------------------------------

        if out_time is None:

            return 0

        if not isinstance(out_time, datetime):

            return 0

        # -----------------------------------------
        # Calculate OT Minutes
        # -----------------------------------------

        overtime_minutes = int(

            (
                out_time -

                self.shift_end

            ).total_seconds() / 60

        )

        # -----------------------------------------
        # Prevent Negative OT
        # -----------------------------------------

        if overtime_minutes < 0:

            overtime_minutes = 0

        return overtime_minutes


    # =====================================================
    # Check Daily OT Status
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

        if overtime_minutes > self.daily_limit:

            employee["daily_status"] = EXCEEDED_STATUS

            employee["daily_message"] = (
                "Daily overtime exceeded company limit."
            )

        elif overtime_minutes == self.daily_limit:

            employee["daily_status"] = LIMIT_REACHED_STATUS

            employee["daily_message"] = (
                "Daily overtime limit reached."
            )

        elif overtime_minutes >= self.daily_warning:

            employee["daily_status"] = WARNING_STATUS

            employee["daily_message"] = (
                "Daily overtime warning."
            )

        else:

            employee["daily_status"] = NORMAL_STATUS

            employee["daily_message"] = (
                "Daily overtime within limit."
            )

        return employee
    # =====================================================
    # Update Monthly Overtime
    # =====================================================

    def update_monthly_ot(
        self,
        employee
    ):

        # -----------------------------------------
        # Update Monthly Database
        # -----------------------------------------

        employee = self.database.update_employee(
            employee
        )

        # -----------------------------------------
        # Get Values
        # -----------------------------------------

        monthly_minutes = int(

            employee.get(

                "monthly_ot_minutes",

                0

            )

        )

        remaining_minutes = int(

            employee.get(

                "remaining_ot_minutes",

                0

            )

        )

        # -----------------------------------------
        # Convert Time
        # -----------------------------------------

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

        if monthly_minutes > self.monthly_limit:

            employee["monthly_status"] = EXCEEDED_STATUS

            employee["monthly_message"] = (

                "Monthly overtime exceeded company limit."

            )

        elif monthly_minutes == self.monthly_limit:

            employee["monthly_status"] = LIMIT_REACHED_STATUS

            employee["monthly_message"] = (

                "Monthly overtime limit reached."

            )

        elif monthly_minutes >= self.monthly_warning:

            employee["monthly_status"] = WARNING_STATUS

            employee["monthly_message"] = (

                "Monthly overtime warning."

            )

        else:

            employee["monthly_status"] = NORMAL_STATUS

            employee["monthly_message"] = (

                "Monthly overtime within limit."

            )

        # -----------------------------------------
        # Dashboard Flags
        # -----------------------------------------

        employee["warning"] = (

            employee["monthly_status"]

            == WARNING_STATUS

        )

        employee["limit_reached"] = (

            employee["monthly_status"]

            == LIMIT_REACHED_STATUS

        )

        employee["ot_exceeded"] = (

            employee["monthly_status"]

            == EXCEEDED_STATUS

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

        # -----------------------------------------
        # Calculate Daily Overtime
        # -----------------------------------------

        daily_ot_minutes = self.calculate_daily_ot(
            out_time
        )

        # -----------------------------------------
        # Daily Validation
        # -----------------------------------------

        employee = self.check_daily_limit(
            employee,
            daily_ot_minutes
        )

        # -----------------------------------------
        # Update Monthly Database
        # -----------------------------------------

        employee = self.update_monthly_ot(
            employee
        )

        # -----------------------------------------
        # Ensure Dashboard Fields
        # -----------------------------------------

        employee.setdefault(
            "daily_ot_minutes",
            0
        )

        employee.setdefault(
            "daily_ot",
            "00:00"
        )

        employee.setdefault(
            "monthly_ot_minutes",
            0
        )

        employee.setdefault(
            "monthly_ot",
            "00:00"
        )

        employee.setdefault(
            "remaining_ot_minutes",
            0
        )

        employee.setdefault(
            "remaining_ot",
            "00:00"
        )

        employee.setdefault(
            "daily_status",
            NORMAL_STATUS
        )

        employee.setdefault(
            "monthly_status",
            NORMAL_STATUS
        )

        employee.setdefault(
            "daily_message",
            ""
        )

        employee.setdefault(
            "monthly_message",
            ""
        )

        employee.setdefault(
            "warning",
            False
        )

        employee.setdefault(
            "limit_reached",
            False
        )

        employee.setdefault(
            "ot_exceeded",
            False
        )

        employee.setdefault(
            "notification_status",
            ""
        )

        return employee