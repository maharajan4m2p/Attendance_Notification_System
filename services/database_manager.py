"""
=========================================================
Attendance Notification System Pro
Enterprise Database Manager
Version : 12.0 Enterprise
=========================================================
"""

import os
from datetime import datetime

import pandas as pd

from config import (
    MONTHLY_OT_DATABASE,
    MONTHLY_DATABASE_COLUMNS,
    MONTHLY_OT_LIMIT_MINUTES,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)


class DatabaseManager:
    """
    Enterprise Monthly OT Database
    One Employee = One Record
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = MONTHLY_OT_DATABASE

        self.columns = MONTHLY_DATABASE_COLUMNS

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
            index=False,
            engine="openpyxl"
        )

    # =====================================================
    # Load Database
    # =====================================================

    def load_database(self):

        if not os.path.exists(self.database):
            self.create_database()

        try:

            dataframe = pd.read_excel(
                self.database,
                engine="openpyxl"
            )

            # Ensure all required columns exist
            for column in self.columns:

                if column not in dataframe.columns:
                    dataframe[column] = ""

            dataframe = dataframe[self.columns]

            dataframe.fillna(
                "",
                inplace=True
            )

            return dataframe

        except Exception as error:

            print(f"Database Error : {error}")

            dataframe = pd.DataFrame(
                columns=self.columns
            )

            dataframe.to_excel(
                self.database,
                index=False,
                engine="openpyxl"
            )

            return dataframe

    # =====================================================
    # Save Database
    # =====================================================

    def save_database(self, dataframe):

        dataframe = dataframe[self.columns]

        dataframe.to_excel(
            self.database,
            index=False,
            engine="openpyxl"
        )
        # =====================================================
    # Find Employee
    # =====================================================

    def find_employee(
        self,
        dataframe,
        employee_id
    ):

        employee_id = str(employee_id).strip()

        if "Employee ID" not in dataframe.columns:
            return None

        dataframe["Employee ID"] = (
            dataframe["Employee ID"]
            .astype(str)
            .str.strip()
        )

        result = dataframe.index[
            dataframe["Employee ID"] == employee_id
        ]

        if len(result) == 0:
            return None

        return int(result[0])

    # =====================================================
    # Employee Exists
    # =====================================================

    def employee_exists(
        self,
        employee_id
    ):

        dataframe = self.load_database()

        return (
            self.find_employee(
                dataframe,
                employee_id
            ) is not None
        )

    # =====================================================
    # Create Employee
    # =====================================================

    def create_employee(
        self,
        dataframe,
        employee
    ):

        record = {}

        # -----------------------------------------
        # Basic Information
        # -----------------------------------------

        record["Employee ID"] = str(
            employee.get(
                "employee_id",
                ""
            )
        ).strip()

        record["Employee Name"] = employee.get(
            "name",
            ""
        )

        record["Department"] = employee.get(
            "department",
            ""
        )

        record["Designation"] = employee.get(
            "designation",
            ""
        )

        record["Email"] = employee.get(
            "email",
            ""
        )

        record["Phone"] = employee.get(
            "phone",
            ""
        )

        # -----------------------------------------
        # Day1 -> Day31
        # -----------------------------------------

        for day in range(1, 32):
            record[f"Day{day}"] = "00:00"

        # -----------------------------------------
        # Monthly Information
        # -----------------------------------------

        record["Monthly OT"] = "00:00"
        record["Monthly OT Minutes"] = 0

        record["Remaining OT"] = "25:00"
        record["Remaining OT Minutes"] = MONTHLY_OT_LIMIT_MINUTES

        record["Monthly Status"] = NORMAL_STATUS

        record["Last Updated"] = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        dataframe.loc[len(dataframe)] = record

        return len(dataframe) - 1
    # =====================================================
    # Get Employee
    # =====================================================

    def get_employee(
        self,
        employee_id
    ):

        dataframe = self.load_database()

        index = self.find_employee(
            dataframe,
            employee_id
        )

        if index is None:
            return None

        employee = dataframe.loc[index].to_dict()

        return employee

    # =====================================================
    # Get All Employees
    # =====================================================

    def get_all_employees(self):

        dataframe = self.load_database()

        return dataframe.to_dict(
            orient="records"
        )

    # =====================================================
    # Convert HH:MM to Minutes
    # =====================================================

    def time_to_minutes(
        self,
        value
    ):

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
    # Convert Minutes to HH:MM
    # =====================================================

    def minutes_to_time(
        self,
        minutes
    ):

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
    # Update Employee
    # =====================================================

    def update_employee(
        self,
        employee
    ):

        dataframe = self.load_database()

        employee_id = str(
            employee.get(
                "employee_id",
                ""
            )
        ).strip()

        index = self.find_employee(
            dataframe,
            employee_id
        )

        if index is None:
            index = self.create_employee(
                dataframe,
                employee
            )

        # ------------------------------------------
        # Update Employee Details
        # ------------------------------------------

        dataframe.at[index, "Employee Name"] = employee.get(
            "name",
            ""
        )

        dataframe.at[index, "Department"] = employee.get(
            "department",
            ""
        )

        dataframe.at[index, "Designation"] = employee.get(
            "designation",
            ""
        )

        dataframe.at[index, "Email"] = employee.get(
            "email",
            ""
        )

        dataframe.at[index, "Phone"] = employee.get(
            "phone",
            ""
        )

        # ------------------------------------------
        # Attendance Date → Day Number
        # ------------------------------------------

        attendance_date = employee.get(
            "attendance_date",
            ""
        )

        try:

            day = pd.to_datetime(
                attendance_date,
                dayfirst=True
            ).day

        except Exception:

            day = datetime.now().day

        day_column = f"Day{day}"

        if day_column not in dataframe.columns:
            dataframe[day_column] = "00:00"

        # ------------------------------------------
        # Save Today's OT
        # ------------------------------------------

        daily_ot = employee.get(
            "daily_ot",
            "00:00"
        )

        if not daily_ot:
            daily_ot = "00:00"

        dataframe.at[
            index,
            day_column
        ] = daily_ot

        # ------------------------------------------
        # Calculate Monthly OT
        # ------------------------------------------

        total_minutes = 0

        for day in range(1, 32):

            column = f"Day{day}"

            if column not in dataframe.columns:
                dataframe[column] = "00:00"

            value = dataframe.at[index, column]

            total_minutes += self.time_to_minutes(
                value
            )

        # ------------------------------------------
        # Monthly OT
        # ------------------------------------------

        monthly_ot = self.minutes_to_time(
            total_minutes
        )

        dataframe.at[
            index,
            "Monthly OT Minutes"
        ] = total_minutes

        dataframe.at[
            index,
            "Monthly OT"
        ] = monthly_ot

        # ------------------------------------------
        # Remaining OT
        # ------------------------------------------

        remaining_minutes = max(
            0,
            MONTHLY_OT_LIMIT_MINUTES - total_minutes
        )

        remaining_ot = self.minutes_to_time(
            remaining_minutes
        )

        dataframe.at[
            index,
            "Remaining OT Minutes"
        ] = remaining_minutes

        dataframe.at[
            index,
            "Remaining OT"
        ] = remaining_ot

        # ------------------------------------------
        # Monthly Status
        # ------------------------------------------

        if total_minutes > MONTHLY_OT_LIMIT_MINUTES:

            status = EXCEEDED_STATUS

        elif total_minutes == MONTHLY_OT_LIMIT_MINUTES:

            status = LIMIT_REACHED_STATUS

        elif total_minutes >= (21 * 60):

            status = WARNING_STATUS

        else:

            status = NORMAL_STATUS

        dataframe.at[
            index,
            "Monthly Status"
        ] = status

        dataframe.at[
            index,
            "Last Updated"
        ] = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        # ------------------------------------------
        # Save Database
        # ------------------------------------------

        self.save_database(
            dataframe
        )

        # ------------------------------------------
        # Return Updated Employee
        # ------------------------------------------

        employee["monthly_ot"] = monthly_ot
        employee["monthly_ot_minutes"] = total_minutes

        employee["remaining_ot"] = remaining_ot
        employee["remaining_ot_minutes"] = remaining_minutes

        employee["monthly_status"] = status

        return employee
    # =====================================================
    # Dashboard Summary
    # =====================================================

    def get_dashboard_summary(self):

        dataframe = self.load_database()

        summary = {
            "total": len(dataframe),
            "present": 0,
            "late_in": 0,
            "early_out": 0,
            "missing_in": 0,
            "missing_out": 0,
            "overtime": 0,
            "monthly_warning": 0,
            "monthly_limit_reached": 0,
            "monthly_ot_exceeded": 0
        }

        if dataframe.empty:
            return summary

        for _, employee in dataframe.iterrows():

            monthly_minutes = int(
                employee.get(
                    "Monthly OT Minutes",
                    0
                )
            )

            if monthly_minutes > 0:
                summary["overtime"] += 1

            status = str(
                employee.get(
                    "Monthly Status",
                    NORMAL_STATUS
                )
            ).strip()

            if status == WARNING_STATUS:
                summary["monthly_warning"] += 1

            elif status == LIMIT_REACHED_STATUS:
                summary["monthly_limit_reached"] += 1

            elif status == EXCEEDED_STATUS:
                summary["monthly_ot_exceeded"] += 1

        return summary

    # =====================================================
    # Monthly Reset
    # =====================================================

    def monthly_reset(self):

        dataframe = self.load_database()

        for index in dataframe.index:

            for day in range(1, 32):
                dataframe.at[index, f"Day{day}"] = "00:00"

            dataframe.at[index, "Monthly OT"] = "00:00"
            dataframe.at[index, "Monthly OT Minutes"] = 0
            dataframe.at[index, "Remaining OT"] = "25:00"
            dataframe.at[index, "Remaining OT Minutes"] = MONTHLY_OT_LIMIT_MINUTES
            dataframe.at[index, "Monthly Status"] = NORMAL_STATUS
            dataframe.at[index, "Last Updated"] = datetime.now().strftime("%d-%b-%Y")

        self.save_database(dataframe)

    # =====================================================
    # Employee Count
    # =====================================================

    def employee_count(self):

        dataframe = self.load_database()

        return len(dataframe)

    # =====================================================
    # Delete Employee
    # =====================================================

    def delete_employee(
        self,
        employee_id
    ):

        dataframe = self.load_database()

        index = self.find_employee(
            dataframe,
            employee_id
        )

        if index is None:
            return False

        dataframe = dataframe.drop(index=index)

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        self.save_database(dataframe)

        return True

    # =====================================================
    # Remove Duplicate Employees
    # =====================================================

    def remove_duplicate_employees(self):

        dataframe = self.load_database()

        dataframe.drop_duplicates(
            subset=["Employee ID"],
            keep="last",
            inplace=True
        )

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        self.save_database(dataframe)

        return len(dataframe)

    # =====================================================
    # Finalize Database
    # =====================================================

    def finalize(self):

        self.remove_duplicate_employees()

        dataframe = self.load_database()

        dataframe.sort_values(
            by="Employee ID",
            inplace=True
        )

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        self.save_database(dataframe)
        