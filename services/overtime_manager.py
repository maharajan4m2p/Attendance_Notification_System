"""
=========================================================
Attendance Notification System Pro
Enterprise Overtime Manager
Version : 15.0 Enterprise
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
    Version 15.0 Enterprise
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
            "-",
            "None",
            "nan",
            "00:00"
        ):
            return 0

        try:

            hh, mm = map(
                int,
                value.split(":")
            )

            return hh * 60 + mm

        except Exception:

            return 0

    # =====================================================
    # Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(self, minutes):

        try:

            minutes = max(
                0,
                int(minutes)
            )

        except Exception:

            minutes = 0

        hh = minutes // 60

        mm = minutes % 60

        return f"{hh:02d}:{mm:02d}"
    # =====================================================
    # Calculate Daily OT
    # =====================================================

    def calculate_daily_overtime(
        self,
        punch_out
    ):

        if punch_out is None:
            return 0

        if not isinstance(
            punch_out,
            datetime
        ):
            return 0

        overtime = int(

            (
                punch_out -
                self.shift_end
            ).total_seconds() / 60

        )

        return max(
            0,
            overtime
        )
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
        # Save employee to Monthly Database
        # DatabaseManager is responsible for:
        #   • Updating today's Day column
        #   • Calculating Monthly OT
        #   • Remaining OT
        #   • Monthly Status
        # ------------------------------------------

        employee = self.database.update_employee(employee)

        # ------------------------------------------
        # Read latest values from database
        # ------------------------------------------

        database_employee = self.database.get_employee(
            employee["employee_id"]
        )

        if database_employee is None:
            return employee

        # ------------------------------------------
        # Copy Day1 - Day31
        # ------------------------------------------

        for day in range(1, 32):

            employee[f"Day{day}"] = database_employee.get(
                f"Day{day}",
                "00:00"
            )

        # ------------------------------------------
        # Copy Monthly Values
        # ------------------------------------------

        employee["monthly_ot"] = database_employee.get(
            "Monthly OT",
            "00:00"
        )

        employee["monthly_ot_minutes"] = int(
            database_employee.get(
                "Monthly OT Minutes",
                0
            )
        )

        employee["remaining_ot"] = database_employee.get(
            "Remaining OT",
            "25:00"
        )

        employee["remaining_ot_minutes"] = int(
            database_employee.get(
                "Remaining OT Minutes",
                self.monthly_limit
            )
        )

        employee["monthly_status"] = database_employee.get(
            "Monthly Status",
            NORMAL_STATUS
        )

        employee["last_updated"] = database_employee.get(
            "Last Updated",
            datetime.now().strftime("%d-%b-%Y %H:%M")
        )

        # ------------------------------------------
        # Dashboard Flags
        # ------------------------------------------

        employee["warning"] = (
            employee["monthly_status"] == WARNING_STATUS
        )

        employee["limit_reached"] = (
            employee["monthly_status"] == LIMIT_REACHED_STATUS
        )

        employee["ot_exceeded"] = (
            employee["monthly_status"] == EXCEEDED_STATUS
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
        # Calculate Today's OT
        # ------------------------------------------

        calculated_ot = self.calculate_daily_overtime(
            punch_out
        )

        imported_ot = self.time_to_minutes(
            employee.get(
                "daily_ot",
                "00:00"
            )
        )

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
        # Save to Monthly Database
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
            employee["monthly_status"]
            == WARNING_STATUS
        )

        employee["is_limit_reached"] = (
            employee["monthly_status"]
            == LIMIT_REACHED_STATUS
        )

        employee["is_exceeded"] = (
            employee["monthly_status"]
            == EXCEEDED_STATUS
        )

        # ------------------------------------------
        # Notification Defaults
        # ------------------------------------------

        employee.setdefault(
            "notification_status",
            "Pending"
        )

        employee.setdefault(
            "notification",
            ""
        )
        
        self.log_employee_summary(employee)
        
        return employee

        # ------------------------------------------
        # Enterprise Debug Log
        # ------------------------------------------

        print("=" * 70)
        print("Employee ID :", employee["employee_id"])
        print("Daily OT    :", employee["daily_ot"])
        print("Monthly OT  :", employee["monthly_ot"])
        print("Status      :", employee["monthly_status"])
        print("=" * 70)

        return employee
    # =====================================================
    # Enterprise Debug Logger
    # =====================================================

    def log_employee_summary(self, employee):

        print("\n" + "=" * 70)
        print("EMPLOYEE OVERTIME SUMMARY")
        print("=" * 70)

        print(f"Employee ID      : {employee.get('employee_id', '')}")
        print(f"Employee Name    : {employee.get('employee_name', '')}")
        print(f"Daily OT         : {employee.get('daily_ot', '00:00')}")
        print(f"Monthly OT       : {employee.get('monthly_ot', '00:00')}")
        print(f"Remaining OT     : {employee.get('remaining_ot', '00:00')}")
        print(f"Monthly Status   : {employee.get('monthly_status', '')}")

        print("-" * 70)

        for day in range(1, 32):
            print(f"Day{day:02d} : {employee.get(f'Day{day}', '00:00')}")

        print("=" * 70)