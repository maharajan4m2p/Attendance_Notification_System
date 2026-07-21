"""
=========================================================
Attendance Notification System Pro
Database Manager
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

import os

from datetime import datetime

import pandas as pd

from config import (
    MONTHLY_OT_DATABASE,
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING,
    LIMIT_REACHED_STATUS,
    WARNING_STATUS,
    NORMAL_STATUS,
    EXCEEDED_STATUS
)


class DatabaseManager:

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = MONTHLY_OT_DATABASE

        self.columns = [

            "Employee ID",

            "Employee Name",

            "Department",

            "Designation",

            "Month",

            "Date",

            "Daily OT Minutes",

            "Monthly OT Minutes",

            "Remaining OT Minutes",

            "Daily Status",

            "Monthly Status",

            "Notification Sent"

        ]

        self.create_database()
        # =====================================================
    # Create Database
    # =====================================================

    def create_database(self):

        if os.path.exists(self.database):
            return

        dataframe = pd.DataFrame(
            columns=self.columns
        )

        dataframe.to_excel(
            self.database,
            index=False
        )

    # =====================================================
    # Load Database
    # =====================================================

    def load(self):

        if not os.path.exists(self.database):

            self.create_database()

        try:

            dataframe = pd.read_excel(
                self.database
            )

        except Exception:

            dataframe = pd.DataFrame(
                columns=self.columns
            )

            dataframe.to_excel(
                self.database,
                index=False
            )

            return dataframe

        # ==========================================
        # Validate Database Columns
        # ==========================================

        if list(dataframe.columns) != self.columns:

            dataframe = dataframe.reindex(
                columns=self.columns,
                fill_value=""
            )

            dataframe.to_excel(
                self.database,
                index=False
            )

        return dataframe
    # =====================================================
    # Save Database
    # =====================================================

    def save(self, dataframe):

        dataframe = dataframe.reindex(
            columns=self.columns,
            fill_value=""
        )

        dataframe.to_excel(
            self.database,
            index=False
        )

    # =====================================================
    # Convert HH:MM -> Minutes
    # =====================================================

    def time_to_minutes(self, value):

        if pd.isna(value):
            return 0

        if value is None:
            return 0

        value = str(value).strip()

        if value in (
            "",
            "-",
            "--",
            "nan",
            "NaN",
            "00:00",
            "00:00:00",
            "0",
            "0.0"
        ):
            return 0

        try:

            parts = value.split(":")

            hours = int(parts[0])

            minutes = int(parts[1])

            return (hours * 60) + minutes

        except Exception:

            return 0

    # =====================================================
    # Convert Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(self, minutes):

        if minutes is None or minutes <= 0:
            return "00:00"

        hours = int(minutes // 60)

        mins = int(minutes % 60)

        return f"{hours:02d}:{mins:02d}"
    # =====================================================
    # Calculate Monthly Total
    # =====================================================

    def calculate_monthly_total(
        self,
        dataframe,
        employee_id,
        month
    ):

        employee_rows = dataframe[
            (dataframe["Employee ID"].astype(str) == str(employee_id))
            &
            (dataframe["Month"].astype(str) == str(month))
        ]

        if employee_rows.empty:
            return 0

        total = pd.to_numeric(
            employee_rows["Daily OT Minutes"],
            errors="coerce"
        ).fillna(0).sum()

        return int(total)

    # =====================================================
    # Calculate Remaining OT
    # =====================================================

    def calculate_remaining_ot(
        self,
        monthly_total
    ):

        monthly_limit = MONTHLY_OT_LIMIT * 60

        remaining = monthly_limit - monthly_total

        if remaining < 0:
            remaining = 0

        return remaining

    # =====================================================
    # Get Monthly Status
    # =====================================================

    def get_monthly_status(
        self,
        monthly_total
    ):

        monthly_limit = MONTHLY_OT_LIMIT * 60

        warning_limit = MONTHLY_OT_WARNING * 60

        if monthly_total > monthly_limit:

            return EXCEEDED_STATUS

        elif monthly_total == monthly_limit:

            return LIMIT_REACHED_STATUS

        elif monthly_total >= warning_limit:

            return WARNING_STATUS

        return NORMAL_STATUS
    # =====================================================
    # Remove Duplicate Attendance
    # =====================================================

    def remove_duplicate(
        self,
        dataframe,
        employee_id,
        attendance_date
    ):

        dataframe = dataframe[

            ~(
                (dataframe["Employee ID"].astype(str) == str(employee_id))
                &
                (dataframe["Date"].astype(str) == str(attendance_date))
            )

        ]

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        return dataframe

    # =====================================================
    # Notification Required
    # =====================================================

    def notification_required(
        self,
        monthly_status
    ):

        if monthly_status == WARNING_STATUS:

            return "Warning"

        elif monthly_status == LIMIT_REACHED_STATUS:

            return "Limit Reached"

        elif monthly_status == EXCEEDED_STATUS:

            return "Exceeded"

        return "No"

    # =====================================================
    # Backup Database
    # =====================================================

    def backup_database(self):

        try:

            backup_file = self.database.replace(
                ".xlsx",
                "_backup.xlsx"
            )

            dataframe = self.load()

            dataframe.to_excel(
                backup_file,
                index=False
            )

        except Exception as error:

            print(
                f"Database Backup Failed : {error}"
            )
            # =====================================================
    # Update Employee Monthly OT
    # =====================================================

    def update_employee(self, employee):

        dataframe = self.load()

        attendance_date = str(
            employee.get(
                "attendance_date",
                datetime.now().strftime("%Y-%m-%d")
            )
        )

        try:

            month = datetime.strptime(
                attendance_date,
                "%Y-%m-%d"
            ).strftime("%Y-%m")

        except Exception:

            month = datetime.now().strftime("%Y-%m")

        employee_id = str(
            employee.get("employee_id", "")
        ).strip()

        employee_name = employee.get(
            "name",
            ""
        )

        department = employee.get(
            "department",
            ""
        )

        designation = employee.get(
            "designation",
            ""
        )

        daily_ot = self.time_to_minutes(
            employee.get(
                "daily_ot",
                "00:00"
            )
        )

        # ==========================================
        # Remove Existing Entry
        # ==========================================

        dataframe = self.remove_duplicate(
            dataframe,
            employee_id,
            attendance_date
        )

        # ==========================================
        # Monthly Calculation
        # ==========================================

        monthly_total = self.calculate_monthly_total(
            dataframe,
            employee_id,
            month
        )

        monthly_total += daily_ot

        remaining_ot = self.calculate_remaining_ot(
            monthly_total
        )

        monthly_status = self.get_monthly_status(
            monthly_total
        )

        # ==========================================
        # Daily Status
        # ==========================================

        if daily_ot > 60:

            daily_status = EXCEEDED_STATUS

        elif daily_ot >= 45:

            daily_status = WARNING_STATUS

        else:

            daily_status = NORMAL_STATUS

        notification = self.notification_required(
            monthly_status
        )

        # ==========================================
        # Create New Row
        # ==========================================

        new_row = {

            "Employee ID": employee_id,

            "Employee Name": employee_name,

            "Department": department,

            "Designation": designation,

            "Month": month,

            "Date": attendance_date,

            "Daily OT Minutes": daily_ot,

            "Monthly OT Minutes": monthly_total,

            "Remaining OT Minutes": remaining_ot,

            "Daily Status": daily_status,

            "Monthly Status": monthly_status,

            "Notification Sent": notification

        }

        dataframe = pd.concat(

            [

                dataframe,

                pd.DataFrame([new_row])

            ],

            ignore_index=True

        )

        self.save(
            dataframe
        )

        self.backup_database()

        # ==========================================
        # Update Employee Dictionary
        # ==========================================

        employee["daily_ot"] = self.minutes_to_time(
            daily_ot
        )

        employee["monthly_ot"] = self.minutes_to_time(
            monthly_total
        )

        employee["remaining_ot"] = self.minutes_to_time(
            remaining_ot
        )

        employee["daily_ot_minutes"] = daily_ot

        employee["monthly_ot_minutes"] = monthly_total

        employee["remaining_ot_minutes"] = remaining_ot

        employee["daily_status"] = daily_status

        employee["monthly_status"] = monthly_status

        employee["notification_status"] = notification

        employee["warning"] = (
            monthly_status == WARNING_STATUS
        )

        employee["limit_reached"] = (
            monthly_status == LIMIT_REACHED_STATUS
        )

        employee["ot_exceeded"] = (
            monthly_status == EXCEEDED_STATUS
        )

        return employee
    # =====================================================
    # Validate Database
    # =====================================================

    def validate_database(self):

        dataframe = self.load()

        dataframe = dataframe.reindex(
            columns=self.columns,
            fill_value=""
        )

        dataframe.drop_duplicates(
            subset=[
                "Employee ID",
                "Date"
            ],
            keep="last",
            inplace=True
        )

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        self.save(dataframe)

        return dataframe

    # =====================================================
    # Get Employee Monthly Summary
    # =====================================================

    def get_employee_summary(
        self,
        employee_id,
        month
    ):

        dataframe = self.load()

        employee_rows = dataframe[

            (dataframe["Employee ID"].astype(str) == str(employee_id))
            &
            (dataframe["Month"].astype(str) == str(month))

        ]

        if employee_rows.empty:

            return {

                "monthly_minutes": 0,

                "remaining_minutes": MONTHLY_OT_LIMIT * 60,

                "status": NORMAL_STATUS

            }

        monthly_minutes = int(
            pd.to_numeric(
                employee_rows["Daily OT Minutes"],
                errors="coerce"
            ).fillna(0).sum()
        )

        remaining = self.calculate_remaining_ot(
            monthly_minutes
        )

        status = self.get_monthly_status(
            monthly_minutes
        )

        return {

            "monthly_minutes": monthly_minutes,

            "remaining_minutes": remaining,

            "status": status

        }

    # =====================================================
    # Reset Monthly Database
    # =====================================================

    def reset_month(self):

        dataframe = pd.DataFrame(
            columns=self.columns
        )

        self.save(dataframe)
        # =====================================================
    # Get Monthly Records
    # =====================================================

    def get_month_records(
        self,
        month
    ):

        dataframe = self.load()

        return dataframe[
            dataframe["Month"].astype(str) == str(month)
        ]

    # =====================================================
    # Get Employee Records
    # =====================================================

    def get_employee_records(
        self,
        employee_id
    ):

        dataframe = self.load()

        return dataframe[
            dataframe["Employee ID"].astype(str)
            == str(employee_id)
        ]

    # =====================================================
    # Check Employee Exists
    # =====================================================

    def employee_exists(
        self,
        employee_id,
        attendance_date
    ):

        dataframe = self.load()

        employee_rows = dataframe[

            (
                dataframe["Employee ID"].astype(str)
                == str(employee_id)
            )

            &

            (
                dataframe["Date"].astype(str)
                == str(attendance_date)
            )

        ]

        return not employee_rows.empty

    # =====================================================
    # Database Statistics
    # =====================================================

    def database_statistics(self):

        dataframe = self.load()

        return {

            "total_records": len(dataframe),

            "employees": dataframe["Employee ID"].nunique(),

            "months": dataframe["Month"].nunique()

        }