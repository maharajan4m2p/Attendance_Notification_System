"""
=========================================================
Attendance Notification System Pro
Database Manager
Version : 8.0 Enterprise (Ultra Performance)
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
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)


class DatabaseManager:
    """
    Enterprise Monthly OT Database Manager

    Features
    --------
    • Single Database Load
    • Duplicate Prevention
    • Monthly OT Tracking
    • Automatic Backup
    • High Performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = MONTHLY_OT_DATABASE

        self.dataframe = None

        self.modified = False

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

        self.load()

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

            index=False,

            engine="openpyxl"

        )

    # =====================================================
    # Load Database
    # =====================================================

    def load(self):

        if self.dataframe is not None:

            return self.dataframe

        if not os.path.exists(

            self.database

        ):

            self.create_database()

        try:

            self.dataframe = pd.read_excel(

                self.database,

                engine="openpyxl"

            )

        except Exception:

            self.dataframe = pd.DataFrame(

                columns=self.columns

            )

        if self.dataframe.empty:

            self.dataframe = pd.DataFrame(

                columns=self.columns

            )

        return self.dataframe

    # =====================================================
    # Convert HH:MM → Minutes
    # =====================================================

    def time_to_minutes(

        self,

        value

    ):

        if value is None:

            return 0

        if pd.isna(value):

            return 0

        value = str(value).strip()

        if value in (

            "",

            "-",

            "--",

            "0",

            "0.0",

            "00:00",

            "00:00:00",

            "nan",

            "NaN",

            "None"

        ):

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
    # Convert Minutes → HH:MM
    # =====================================================

    def minutes_to_time(

        self,

        minutes

    ):

        if minutes is None:

            return "00:00"

        if minutes <= 0:

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

            (

                dataframe["Employee ID"] == employee_id

            )

            &

            (

                dataframe["Month"] == month

            )

        ]

        if employee_rows.empty:

            return 0

        return int(

            employee_rows[

                "Daily OT Minutes"

            ].sum()

        )

    # =====================================================
    # Calculate Remaining OT
    # =====================================================

    def calculate_remaining_ot(

        self,

        monthly_total

    ):

        remaining = (

            MONTHLY_OT_LIMIT * 60

        ) - monthly_total

        return max(

            0,

            remaining

        )

    # =====================================================
    # Get Monthly Status
    # =====================================================

    def get_monthly_status(

        self,

        monthly_total

    ):

        limit = MONTHLY_OT_LIMIT * 60

        warning = MONTHLY_OT_WARNING * 60

        if monthly_total > limit:

            return EXCEEDED_STATUS

        elif monthly_total == limit:

            return LIMIT_REACHED_STATUS

        elif monthly_total >= warning:

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

        dataframe = dataframe.loc[

            ~

            (

                (

                    dataframe["Employee ID"] == employee_id

                )

                &

                (

                    dataframe["Date"] == attendance_date

                )

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

        return ""

    # =====================================================
    # Backup Database
    # =====================================================

    def backup_database(self):

        if self.dataframe is None:

            return

        try:

            backup_file = self.database.replace(

                ".xlsx",

                "_backup.xlsx"

            )

            self.dataframe.to_excel(

                backup_file,

                index=False,

                engine="openpyxl"

            )

        except Exception as error:

            print("=" * 60)

            print(

                f"Backup Failed : {error}"

            )

            print("=" * 60)
            # =====================================================
    # Update Employee
    # =====================================================

    def update_employee(

        self,

        employee

    ):

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

            employee.get(

                "employee_id",

                ""

            )

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

        # -----------------------------------------
        # Remove Duplicate Record
        # -----------------------------------------

        dataframe = self.remove_duplicate(

            dataframe,

            employee_id,

            attendance_date

        )

        # -----------------------------------------
        # Calculate Monthly OT
        # -----------------------------------------

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

        # -----------------------------------------
        # Daily Status
        # -----------------------------------------

        if daily_ot > 60:

            daily_status = EXCEEDED_STATUS

        elif daily_ot == 60:

            daily_status = LIMIT_REACHED_STATUS

        elif daily_ot >= 45:

            daily_status = WARNING_STATUS

        else:

            daily_status = NORMAL_STATUS

        notification = self.notification_required(

            monthly_status

        )

        # -----------------------------------------
        # Add Employee Record
        # -----------------------------------------

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

        # -----------------------------------------
        # Update Memory
        # -----------------------------------------

        self.dataframe = dataframe

        self.modified = True

        # -----------------------------------------
        # Update Employee Object
        # -----------------------------------------

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
    # Save Database
    # =====================================================

    def save(self):

        if self.dataframe is None:

            return

        if not self.modified:

            return

        print("=" * 60)
        print("Saving Monthly OT Database...")
        print("=" * 60)

        self.dataframe.to_excel(

            self.database,

            index=False,

            engine="openpyxl"

        )

        self.modified = False

        self.backup_database()

        print("=" * 60)
        print("Database Saved Successfully")
        print("=" * 60)

    # =====================================================
    # Finalize Database
    # =====================================================

    def finalize(self):

        self.save()

        print("=" * 60)
        print("Monthly OT Database Updated Successfully")
        print("=" * 60)