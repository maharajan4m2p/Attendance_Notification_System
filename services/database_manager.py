"""
=========================================================
Attendance Notification System Pro
Enterprise Database Manager
Version : 13.0 Enterprise
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
    Enterprise Version 13.0
    Optimized Performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = MONTHLY_OT_DATABASE

        self.columns = MONTHLY_DATABASE_COLUMNS

        self._cached_dataframe = None

        self._cache_loaded = False

        self.create_database()

    # =====================================================
    # Get Cached Database
    # =====================================================

    def _get_dataframe(self):

        if (

            self._cache_loaded

            and self._cached_dataframe is not None

        ):

            return self._cached_dataframe.copy()

        dataframe = self.load_database()

        self._cached_dataframe = dataframe.copy()

        self._cache_loaded = True

        return dataframe

    # =====================================================
    # Clear Cache
    # =====================================================

    def _clear_cache(self):

        self._cached_dataframe = None

        self._cache_loaded = False
        # =====================================================
# Create Database
# =====================================================

    def create_database(self):

        if os.path.exists(self.database):

            return

        dataframe = pd.DataFrame(

            columns=self.columns

        )

        with pd.ExcelWriter(

            self.database,

            engine="openpyxl",

            mode="w"

        ) as writer:

            dataframe.to_excel(

                writer,

                index=False,

                sheet_name="Monthly OT Database"

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

        except Exception:

            dataframe = pd.DataFrame(

            columns=self.columns

            )

    # -----------------------------------------
    # Ensure Required Columns
    # -----------------------------------------

        for column in self.columns:

            if column not in dataframe.columns:

                dataframe[column] = ""

        dataframe = dataframe[self.columns]

        dataframe.fillna(

            "",

            inplace=True

        )

        dataframe["Employee ID"] = (

            dataframe["Employee ID"]

            .astype(str)

            .str.strip()

        )

        dataframe["Monthly OT Minutes"] = pd.to_numeric(

            dataframe["Monthly OT Minutes"],

            errors="coerce"

        ).fillna(0).astype(int)

        dataframe["Remaining OT Minutes"] = pd.to_numeric(

            dataframe["Remaining OT Minutes"],

            errors="coerce"

        ).fillna(MONTHLY_OT_LIMIT_MINUTES).astype(int)

        return dataframe
    # =====================================================
# Save Database
# =====================================================

    def save_database(
        self,
        dataframe
    ):

        dataframe = dataframe[self.columns]

        with pd.ExcelWriter(

            self.database,

            engine="openpyxl",

            mode="w"

        ) as writer:

            dataframe.to_excel(

                writer,

                index=False,

                sheet_name="Monthly OT Database"

            )

        self._cached_dataframe = dataframe.copy()

        self._cache_loaded = True


# =====================================================
# Find Employee
# =====================================================

    def find_employee(

        self,

        dataframe,

        employee_id

    ):

        if dataframe.empty:

            return None

        employee_id = str(employee_id).strip()

        matches = dataframe.index[

            dataframe["Employee ID"]

            .astype(str)

            .str.strip()

            == employee_id

        ]

        if len(matches) == 0:

            return None

        return int(matches[0])


# =====================================================
# Employee Exists
# =====================================================

    def employee_exists(

        self,

        employee_id

    ):

        dataframe = self._get_dataframe()

        return (

            self.find_employee(

                dataframe,

                employee_id

            )

            is not None

        )


# =====================================================
# Get Employee
# =====================================================

    def get_employee(

        self,

        employee_id

    ):

        dataframe = self._get_dataframe()

        index = self.find_employee(

            dataframe,

            employee_id

        )

        if index is None:

            return None

        employee = dataframe.loc[

            index

        ].to_dict()

        return employee


# =====================================================
# Get All Employees
# =====================================================

    def get_all_employees(self):

        dataframe = self._get_dataframe()

        return dataframe.to_dict(

            orient="records"
        )
        # =====================================================
        # Convert HH:MM to Minutes
        # =====================================================

    def time_to_minutes(self, value):

        if value is None:
            return 0

        value = str(value).strip()

        if value in ("", "00:00", "-", "None", "nan"):
            return 0

        try:
            hours, minutes = map(int, value.split(":"))
            return (hours * 60) + minutes
        except Exception:
            return 0


        # =====================================================
        # Convert Minutes to HH:MM
        # =====================================================

    def minutes_to_time(self, minutes):

        try:
            minutes = max(0, int(minutes))
        except Exception:
            minutes = 0

        hours = minutes // 60
        mins = minutes % 60

        return f"{hours:02d}:{mins:02d}"

    # =====================================================
    # Create Employee
    # =====================================================

    def create_employee(

        self,

        dataframe,

        employee

    ):

        record = {

            "Employee ID": str(

                employee.get(

                    "employee_id",

                    ""

                )

            ).strip(),

            "Employee Name": employee.get(

                "name",

                ""

            ),

            "Department": employee.get(

                "department",

                ""

            ),

            "Designation": employee.get(

                "designation",

                ""

            ),

            "Email": employee.get(

                "email",

                ""

            ),

            "Phone": employee.get(

                "phone",

                ""

            )

        }

    # -----------------------------------------
    # Day1 → Day31
    # -----------------------------------------

        record.update({

            f"Day{i}": "00:00"

            for i in range(1, 32)

        })

    # -----------------------------------------
    # Monthly Information
    # -----------------------------------------

        record.update({

            "Monthly OT": "00:00",

            "Monthly OT Minutes": 0,

            "Remaining OT": self.minutes_to_time(

                MONTHLY_OT_LIMIT_MINUTES

            ),

            "Remaining OT Minutes": MONTHLY_OT_LIMIT_MINUTES,

            "Monthly Status": NORMAL_STATUS,

            "Last Updated": datetime.now().strftime(

                "%d-%b-%Y %H:%M"

            )

        })

        dataframe.loc[

            len(dataframe)

        ] = record

        return len(dataframe) - 1
    
        # =====================================================
        # Update Employee
        # =====================================================


    def update_employee(
        self,
        employee
    ):

        dataframe = self._get_dataframe()

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
        # Update Basic Information
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
        # Attendance Date
        # ------------------------------------------

        attendance_date = employee.get(
            "attendance_date",
            ""
        )

        try:

            attendance_date = pd.to_datetime(
                attendance_date,
                dayfirst=True
            )

            day = attendance_date.day
            month = attendance_date.month
            year = attendance_date.year

        except Exception:

            today = datetime.now()

            day = today.day
            month = today.month
            year = today.year
            # ------------------------------------------
    # Monthly Reset (New Month Only)
    # ------------------------------------------

        last_updated = str(

            dataframe.at[index, "Last Updated"]

        )

        try:

            last_date = pd.to_datetime(

                last_updated,

                dayfirst=True

            )

            if (

                last_date.month != month

                or

                last_date.year != year

            ):

                for i in range(1, 32):

                    dataframe.at[

                        index,

                        f"Day{i}"

                    ] = "00:00"

        except Exception:

            pass

        # ------------------------------------------
        # Save Today's OT
        # ------------------------------------------

        day_column = f"Day{day}"

        daily_ot = employee.get(
            "daily_ot",
            "00:00"
        )
        
        if not daily_ot:
            daily_ot = "00:00"
            
        dataframe.at[index, day_column] = daily_ot
            # ------------------------------------------
            # Calculate Monthly OT
            # ------------------------------------------

        total_minutes = 0

        for i in range(1, 32):

            value = dataframe.at[index, f"Day{i}"]
            
            total_minutes += self.time_to_minutes(value)
            
        monthly_ot = self.minutes_to_time(

            total_minutes

        )

        remaining_minutes = max(

            0,

            MONTHLY_OT_LIMIT_MINUTES - total_minutes

        )

        remaining_ot = self.minutes_to_time(

            remaining_minutes

        )

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

        # ------------------------------------------
        # Update Database
        # ------------------------------------------

        dataframe.at[index, "Monthly OT"] = monthly_ot

        dataframe.at[index, "Monthly OT Minutes"] = total_minutes

        dataframe.at[index, "Remaining OT"] = remaining_ot

        dataframe.at[index, "Remaining OT Minutes"] = remaining_minutes

        dataframe.at[index, "Monthly Status"] = status

        dataframe.at[index, "Last Updated"] = datetime.now().strftime(

            "%d-%b-%Y %H:%M"

        )

        # ------------------------------------------
        # Save Database
        # ------------------------------------------

        self.save_database(

            dataframe

        )
        
        self._clear_cache()
        
        dataframe = self._get_dataframe()

        # ------------------------------------------
        # Update Employee Dictionary
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

        dataframe = self._get_dataframe()

        summary = {

            "total": len(dataframe),

            "present": 0,

            "absent": 0,

            "half_day": 0,

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

        summary["overtime"] = int(

            dataframe["Monthly OT Minutes"]

            .fillna(0)

            .astype(int)

            .gt(0)

            .sum()

        )

        status_counts = dataframe["Monthly Status"].value_counts()

        summary["monthly_warning"] = int(

            status_counts.get(

                WARNING_STATUS,

                0

            )

        )

        summary["monthly_limit_reached"] = int(

            status_counts.get(

                LIMIT_REACHED_STATUS,

                0

            )

        )

        summary["monthly_ot_exceeded"] = int(

            status_counts.get(

                EXCEEDED_STATUS,

                0

            )

        )

        return summary


# =====================================================
# Monthly Reset
# =====================================================

    def monthly_reset(self):

        dataframe = self._get_dataframe()

        if dataframe.empty:

            return False

    # -----------------------------------------
    # Reset Daily OT (Day1-Day31)
    # -----------------------------------------

        for day in range(1, 32):

            dataframe[f"Day{day}"] = "00:00"

    # -----------------------------------------
    # Reset Monthly Information
    # -----------------------------------------

        dataframe["Monthly OT"] = "00:00"

        dataframe["Monthly OT Minutes"] = 0

        dataframe["Remaining OT"] = self.minutes_to_time(

            MONTHLY_OT_LIMIT_MINUTES

        )

        dataframe["Remaining OT Minutes"] = MONTHLY_OT_LIMIT_MINUTES

        dataframe["Monthly Status"] = NORMAL_STATUS

        dataframe["Last Updated"] = datetime.now().strftime(

            "%d-%b-%Y %H:%M"

        )

    # -----------------------------------------
    # Save Database
    # -----------------------------------------

        self.save_database(

            dataframe

        )

        return True

# =====================================================
# Employee Count
# =====================================================

    def employee_count(self):

        return len(

            self._get_dataframe()

        )


# =====================================================
# Delete Employee
# =====================================================

    def delete_employee(

        self,

        employee_id

    ):

        dataframe = self._get_dataframe()

        index = self.find_employee(

            dataframe,

            employee_id

        )

        if index is None:

            return False

        dataframe.drop(

            index=index,

            inplace=True

        )

        dataframe.reset_index(

            drop=True,

            inplace=True

        )

        self.save_database(

            dataframe

        )

        return True


# =====================================================
# Remove Duplicate Employees
# =====================================================

    def remove_duplicate_employees(self):

        dataframe = self._get_dataframe()

        if dataframe.empty:

            return 0

        dataframe.drop_duplicates(

            subset=["Employee ID"],

            keep="last",

            inplace=True

        )

        dataframe.sort_values(

            by="Employee ID",

            inplace=True

        )

        dataframe.reset_index(

            drop=True,

            inplace=True

        )

        self.save_database(

            dataframe

        )

        return len(dataframe)


# =====================================================
# Finalize Database
# =====================================================

    def finalize(self):

        self.remove_duplicate_employees()

        dataframe = self._get_dataframe()

        if dataframe.empty:

            return

        dataframe.sort_values(

            by="Employee ID",

            inplace=True

        )

        dataframe.reset_index(

            drop=True,

            inplace=True

        )

        self.save_database(

            dataframe

        )

        self._clear_cache()