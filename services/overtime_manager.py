"""
=========================================================
Attendance Notification System Pro
Enterprise Overtime Manager
Version : 13.0 Enterprise
=========================================================
"""

from datetime import datetime

from config import (
    SHIFT_END,
    DAILY_OT_WARNING,
    DAILY_OT_LIMIT,
    MONTHLY_OT_WARNING_MINUTES,
    MONTHLY_OT_LIMIT_MINUTES,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)

from services.database_manager import DatabaseManager


class OvertimeManager:
    """
    Enterprise Overtime Processing Engine
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = DatabaseManager()

        self.shift_end = datetime.strptime(
            SHIFT_END,
            "%H:%M"
        )

        self.daily_warning = DAILY_OT_WARNING
        self.daily_limit = DAILY_OT_LIMIT

        self.monthly_warning = MONTHLY_OT_WARNING_MINUTES
        self.monthly_limit = MONTHLY_OT_LIMIT_MINUTES

    # =====================================================
    # HH:MM -> Minutes
    # =====================================================

    def time_to_minutes(self, value):

        if value is None:
            return 0

        value = str(value).strip()

        if value in (
            "",
            "00:00",
            "nan",
            "None",
            "-"
        ):
            return 0

        try:

            hours, minutes = value.split(":")

            return (
                int(hours) * 60 +
                int(minutes)
            )

        except Exception:

            return 0

    # =====================================================
    # Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(self, minutes):

        try:
            minutes = int(minutes)
        except Exception:
            minutes = 0

        if minutes < 0:
            minutes = 0

        hours = minutes // 60
        mins = minutes % 60

        return f"{hours:02d}:{mins:02d}"

    # =====================================================
    # Calculate Daily Overtime
    # =====================================================

    def calculate_daily_overtime(self, punch_out):

        if punch_out is None:
            return 0

        if not isinstance(
            punch_out,
            datetime
        ):
            return 0

        overtime_minutes = int(
            (
                punch_out -
                self.shift_end
            ).total_seconds() / 60
        )

        if overtime_minutes < 0:
            overtime_minutes = 0

        return overtime_minutes
    # =====================================================
    # Check Late Punch
    # =====================================================

    def is_late_punch(
        self,
        punch_in,
        grace_time
    ):

        if punch_in is None:
            return False

        if not isinstance(
            punch_in,
            datetime
        ):
            return False

        return punch_in > grace_time

    # =====================================================
    # Check Early Out
    # =====================================================

    def is_early_out(
        self,
        punch_out
    ):

        if punch_out is None:
            return False

        if not isinstance(
            punch_out,
            datetime
        ):
            return False

        return punch_out < self.shift_end

    # =====================================================
    # Daily OT Status
    # =====================================================

    def get_daily_status(
        self,
        overtime_minutes
    ):

        overtime_minutes = max(
            0,
            int(overtime_minutes)
        )

        if overtime_minutes > self.daily_limit:

            return (
                EXCEEDED_STATUS,
                f"Daily OT exceeded ({self.minutes_to_time(overtime_minutes)})"
            )

        elif overtime_minutes == self.daily_limit:

            return (
                LIMIT_REACHED_STATUS,
                f"Daily OT limit reached ({self.minutes_to_time(overtime_minutes)})"
            )

        elif overtime_minutes >= self.daily_warning:

            return (
                WARNING_STATUS,
                f"Daily OT warning ({self.minutes_to_time(overtime_minutes)})"
            )

        return (
            NORMAL_STATUS,
            "Daily OT within limit."
        )
        # =====================================================
    # Update Monthly Overtime
    # =====================================================

    def update_monthly_overtime(
        self,
        employee
    ):

        # ------------------------------------------
        # Update Employee in Database
        # ------------------------------------------

        employee = self.database.update_employee(
            employee
        )

        # ------------------------------------------
        # Monthly OT
        # ------------------------------------------

        employee["monthly_ot"] = employee.get(
            "monthly_ot",
            "00:00"
        )

        employee["monthly_ot_minutes"] = employee.get(
            "monthly_ot_minutes",
            0
        )

        # ------------------------------------------
        # Remaining OT
        # ------------------------------------------

        employee["remaining_ot"] = employee.get(
            "remaining_ot",
            "25:00"
        )

        employee["remaining_ot_minutes"] = employee.get(
            "remaining_ot_minutes",
            self.monthly_limit
        )

        # ------------------------------------------
        # Monthly Status
        # ------------------------------------------

        status = employee.get(
            "monthly_status",
            NORMAL_STATUS
        )

        employee["monthly_status"] = status

        # ------------------------------------------
        # Dashboard Flags
        # ------------------------------------------

        employee["warning"] = (
            status == WARNING_STATUS
        )

        employee["limit_reached"] = (
            status == LIMIT_REACHED_STATUS
        )

        employee["ot_exceeded"] = (
            status == EXCEEDED_STATUS
        )

        employee["last_updated"] = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        return employee
    # =====================================================
    # Process Employee Overtime
    # =====================================================

    def process(
        self,
        employee,
        punch_out,
        day=None
    ):

        # ------------------------------------------
        # Calculate OT from Punch Out
        # ------------------------------------------

        calculated_ot = self.calculate_daily_overtime(
            punch_out
        )

        # ------------------------------------------
        # Imported OT from Attendance File
        # ------------------------------------------

        imported_ot = self.time_to_minutes(
            employee.get(
                "daily_ot",
                "00:00"
            )
        )

        # ------------------------------------------
        # Use Higher OT Value
        # ------------------------------------------

        overtime_minutes = max(
            calculated_ot,
            imported_ot
        )

        employee["daily_ot_minutes"] = overtime_minutes

        employee["daily_ot"] = self.minutes_to_time(
            overtime_minutes
        )

        # ------------------------------------------
        # Daily Status
        # ------------------------------------------

        status, message = self.get_daily_status(
            overtime_minutes
        )

        employee["daily_status"] = status
        employee["daily_message"] = message

        # ------------------------------------------
        # Update Monthly Database
        # ------------------------------------------

        employee = self.update_monthly_overtime(
            employee
        )

        # ------------------------------------------
        # Dashboard Flags
        # ------------------------------------------

        employee["is_overtime"] = (
            overtime_minutes > 0
        )

        employee["is_warning"] = (
            employee["monthly_status"] == WARNING_STATUS
        )

        employee["is_limit_reached"] = (
            employee["monthly_status"] == LIMIT_REACHED_STATUS
        )

        employee["is_exceeded"] = (
            employee["monthly_status"] == EXCEEDED_STATUS
        )

        # ------------------------------------------
        # Notification
        # ------------------------------------------

        employee.setdefault(
            "notification_status",
            "Pending"
        )

        employee.setdefault(
            "notification",
            ""
        )

        # ------------------------------------------
        # Copy Day1-Day31 values from Database
        # ------------------------------------------

        database_employee = self.database.get_employee(
            employee["employee_id"]
        )

        if database_employee:

            for day_number in range(1, 32):

                column = f"Day{day_number}"

                employee[column] = database_employee.get(
                    column,
                    "00:00"
                )

            employee["monthly_ot"] = database_employee.get(
                "Monthly OT",
                employee["monthly_ot"]
            )

            employee["monthly_ot_minutes"] = database_employee.get(
                "Monthly OT Minutes",
                employee["monthly_ot_minutes"]
            )

            employee["remaining_ot"] = database_employee.get(
                "Remaining OT",
                employee["remaining_ot"]
            )

            employee["remaining_ot_minutes"] = database_employee.get(
                "Remaining OT Minutes",
                employee["remaining_ot_minutes"]
            )

            employee["monthly_status"] = database_employee.get(
                "Monthly Status",
                employee["monthly_status"]
            )

        return employee