"""
=========================================================
Attendance Notification System Pro
Database Manager
Version : 10.0 Enterprise
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
    • Monthly OT Tracking
    • Employee History
    • Duplicate Prevention
    • Automatic Backup
    • High Performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = MONTHLY_OT_DATABASE
        
        print("=" * 60)
        print("Database File")
        print(self.database)
        print("=" * 60)

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

        # Create database if it does not exist
        self.create_database()

        # Load database into memory
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

        print("=" * 60)
        print("Monthly OT Database Created Successfully")
        print("=" * 60)

    # =====================================================
    # Load Database
    # =====================================================

    def load(self):

        if self.dataframe is not None:

            return self.dataframe

        if not os.path.exists(self.database):

            self.create_database()

        try:

            self.dataframe = pd.read_excel(

                self.database,

                engine="openpyxl"

            )
        
            print("=" * 60)
            print("MONTHLY OT DATABASE LOADED")
            print(f"Database Path : {self.database}")
            print(f"Records Loaded: {len(self.dataframe)}")
            print("First 5 Records:")
            print(self.dataframe.head())
            print("=" * 60)

        except Exception as error:

            print("=" * 60)
            print(f"Database Load Failed : {error}")
            print("Creating Empty Database...")
            print("=" * 60)

            self.dataframe = pd.DataFrame(

                columns=self.columns

            )

        # -----------------------------------------
        # Ensure Required Columns
        # -----------------------------------------

        for column in self.columns:

            if column not in self.dataframe.columns:

                self.dataframe[column] = ""

        self.dataframe = self.dataframe[

            self.columns

        ]

        self.dataframe.fillna(

            "",

            inplace=True

        )

        # -----------------------------------------
        # Convert Numeric Columns
        # -----------------------------------------

        numeric_columns = [

            "Daily OT Minutes",

            "Monthly OT Minutes",

            "Remaining OT Minutes"

        ]

        for column in numeric_columns:

            self.dataframe[column] = pd.to_numeric(

                self.dataframe[column],

                errors="coerce"

            ).fillna(0).astype(int)

        print("=" * 60)
        print(

            f"Monthly OT Records Loaded : {len(self.dataframe)}"

        )
        print("=" * 60)

        return self.dataframe
    # =====================================================
    # Convert HH:MM -> Minutes
    # =====================================================

    def time_to_minutes(
        self,
        value
    ):

        if value is None:
            return 0

        if pd.isna(value):
            return 0

        # -----------------------------------------
        # Already Numeric
        # -----------------------------------------

        if isinstance(value, (int, float)):

            return int(value)

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

            "None",

            "N/A"

        ):

            return 0

        # -----------------------------------------
        # HH:MM
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
        # Decimal Minutes
        # -----------------------------------------

        try:

            return int(float(value))

        except Exception:

            return 0


    # =====================================================
    # Convert Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(
        self,
        minutes
    ):

        try:

            minutes = int(minutes)

        except Exception:

            return "00:00"

        if minutes <= 0:

            return "00:00"

        hours = minutes // 60

        mins = minutes % 60

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

        if dataframe.empty:

            return 0

        employee_rows = dataframe.loc[

            (
                dataframe["Employee ID"].astype(str)
                ==
                str(employee_id)
            )

            &

            (
                dataframe["Month"].astype(str)
                ==
                str(month)
            )

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

        return max(
            monthly_limit - monthly_total,
            0
        )

    # =====================================================
    # Get Monthly Status
    # =====================================================

    def get_monthly_status(
        self,
        monthly_total
    ):

        monthly_limit = MONTHLY_OT_LIMIT * 60

        remaining = monthly_limit - monthly_total

        if monthly_total > monthly_limit:
            return EXCEEDED_STATUS

        elif monthly_total == monthly_limit:
            return LIMIT_REACHED_STATUS

        # Warning only when 3 hours or less remain
        elif remaining <= 180:
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

        if dataframe.empty:

            return dataframe

        dataframe = dataframe.loc[

            ~(
                (
                    dataframe["Employee ID"].astype(str)
                    ==
                    str(employee_id)
                )

                &

                (
                    dataframe["Date"].astype(str)
                    ==
                    str(attendance_date)
                )
            )

        ].copy()

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

        if self.dataframe.empty:

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
            print("=" * 60)
            print("MONTHLY OT DATABASE SAVED")
            print(f"Database Path : {self.database}")
            print(f"Records Saved : {len(self.dataframe)}")
            print("=" * 60)

            print("=" * 60)
            print("Monthly OT Backup Created Successfully")
            print("=" * 60)

        except Exception as error:

            print("=" * 60)
            print(f"Database Backup Failed : {error}")
            print("=" * 60)
            # =====================================================
    # Update Employee
    # =====================================================

    def update_employee(
        self,
        employee
    ):

        dataframe = self.load()

        employee_id = str(
            employee.get(
                "employee_id",
                ""
            )
        ).strip()

        employee_name = str(
            employee.get(
                "name",
                ""
            )
        ).strip()

        department = str(
            employee.get(
                "department",
                ""
            )
        ).strip()

        designation = str(
            employee.get(
                "designation",
                ""
            )
        ).strip()

        attendance_date = str(
            employee.get(
                "attendance_date",
                datetime.now().strftime("%Y-%m-%d")
            )
        ).strip()

        # -----------------------------------------
        # Month
        # -----------------------------------------

        try:

            month = datetime.strptime(

                attendance_date,

                "%Y-%m-%d"

            ).strftime("%Y-%m")

        except Exception:

            month = datetime.now().strftime("%Y-%m")

        # -----------------------------------------
        # Daily OT Minutes
        # -----------------------------------------

        daily_ot_minutes = employee.get(

            "daily_ot_minutes",

            None

        )

        if daily_ot_minutes is None:

            daily_ot_minutes = self.time_to_minutes(

                employee.get(

                    "daily_ot",

                    "00:00"

                )

            )
        if isinstance(daily_ot_minutes, str):
            daily_ot_minutes = self.time_to_minutes(daily_ot_minutes)
        daily_ot_minutes = int(daily_ot_minutes)

        # -----------------------------------------
        # Remove Duplicate Record
        # -----------------------------------------

        dataframe = self.remove_duplicate(

            dataframe,

            employee_id,

            attendance_date

        )

        # -----------------------------------------
        # Monthly OT
        # -----------------------------------------

        previous_total = self.calculate_monthly_total(

            dataframe,

            employee_id,

            month

        )

        # Previous OT before today's upload
        employee["previous_ot_minutes"] = previous_total
        employee["previous_ot"] = self.minutes_to_time(
            previous_total
        )

        monthly_total = previous_total + daily_ot_minutes
        remaining_ot = max(
            (MONTHLY_OT_LIMIT * 60) - monthly_total,
            0
            )
        monthly_status = self.get_monthly_status(
            monthly_total
        )

        # -----------------------------------------
        # Daily Status
        # -----------------------------------------

        if daily_ot_minutes > 60:

            daily_status = EXCEEDED_STATUS

        elif daily_ot_minutes == 60:

            daily_status = LIMIT_REACHED_STATUS

        elif daily_ot_minutes >= 45:

            daily_status = WARNING_STATUS

        else:

            daily_status = NORMAL_STATUS

        notification = self.notification_required(

            monthly_status

        )

        # -----------------------------------------
        # Save Record
        # -----------------------------------------

        new_row = {

            "Employee ID": employee_id,

            "Employee Name": employee_name,

            "Department": department,

            "Designation": designation,

            "Month": month,

            "Date": attendance_date,

            "Daily OT Minutes": daily_ot_minutes,

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

        self.dataframe = dataframe

        self.modified = True

        # -----------------------------------------
        # Update Employee Dictionary
        # -----------------------------------------

        employee["daily_ot_minutes"] = daily_ot_minutes
        
        employee["previous_ot_minutes"] = previous_total

        employee["monthly_ot_minutes"] = monthly_total

        employee["remaining_ot_minutes"] = self.minutes_to_time(
            remaining_ot
        )

        employee["daily_ot"] = self.minutes_to_time(

            daily_ot_minutes

        )
        
        employee["previous_ot"] = self.minutes_to_time(
        
            previous_total
        
        )
        

        employee["monthly_ot"] = self.minutes_to_time(

            monthly_total

        )

        employee["remaining_ot"] = self.minutes_to_time(

            remaining_ot

        )

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
        print("=" * 60)
        print("DATABASE UPDATED")
        print(f"Employee ID : {employee_id}")
        print(f"Date        : {attendance_date}")
        print(f"Previous OT : {previous_total}")
        print(f"Daily OT    : {daily_ot_minutes}")
        print(f"Monthly OT  : {monthly_total}")
        print(f"Status      : {monthly_status}")
        print("=" * 60)

        return employee
    # =====================================================
    # Save Database
    # =====================================================

    def save(self):

        if self.dataframe is None:

            return

        if not self.modified:

            print("=" * 60)
            print("No Database Changes Found")
            print("=" * 60)

            return

        try:

            print("=" * 60)
            print("Saving Monthly OT Database...")
            print("=" * 60)

            # -----------------------------------------
            # Sort Records
            # -----------------------------------------

            self.dataframe["Employee ID"] = (
                self.dataframe["Employee ID"]
                .astype(str)
            )

            self.dataframe["Month"] = (
                self.dataframe["Month"]
                .astype(str)
            )

            self.dataframe["Date"] = (
                self.dataframe["Date"]
                .astype(str)
            )

            self.dataframe.sort_values(

                by=[

                    "Employee ID",

                    "Month",

                    "Date"

                ],

                ascending=True,

                inplace=True,

                ignore_index=True

            )

            # -----------------------------------------
            # Save Excel
            # -----------------------------------------

            self.dataframe.to_excel(

                self.database,

                index=False,

                engine="openpyxl"

            )
            
            print("=" * 60)
            print("MONTHLY OT DATABASE SAVED")
            print(f"Database Path : {self.database}")
            print(f"Records Saved : {len(self.dataframe)}")
            print("=" * 60)

            self.modified = False

            # -----------------------------------------
            # Backup
            # -----------------------------------------

            self.backup_database()

            print("=" * 60)
            print("Monthly OT Database Saved Successfully")
            print("=" * 60)

        except Exception as error:

            print("=" * 60)
            print(f"Database Save Failed : {error}")
            print("=" * 60)


    # =====================================================
    # Finalize Database
    # =====================================================

    def finalize(self):

        self.save()

        print("=" * 60)
        print("Monthly OT Database Finalized")
        print("=" * 60)