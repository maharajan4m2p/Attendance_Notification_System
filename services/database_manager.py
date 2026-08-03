"""
=========================================================
Attendance Notification System Pro
Enterprise Database Manager
Version : 15.0 Enterprise
=========================================================
"""

import os
from datetime import datetime

from numpy.strings import index
import pandas as pd

from config import (
    MONTHLY_OT_DATABASE,
    MONTHLY_DATABASE_COLUMNS,
    MONTHLY_OT_LIMIT_MINUTES,
    MONTHLY_OT_WARNING_MINUTES,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)


class DatabaseManager:
    """
    Enterprise Monthly OT Database
    Version 15.0 Enterprise
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
    # Cache
    # =====================================================

    def _clear_cache(self):

        self._cached_dataframe = None
        self._cache_loaded = False

    def _get_dataframe(self):

        if self._cache_loaded and self._cached_dataframe is not None:
            return self._cached_dataframe.copy()

        dataframe = self.load_database()

        self._cached_dataframe = dataframe.copy()
        self._cache_loaded = True

        return dataframe

    # =====================================================
    # Create Database
    # =====================================================

    def create_database(self):

        if os.path.exists(self.database):
            return

        dataframe = pd.DataFrame(columns=self.columns)

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

        for column in self.columns:

            if column not in dataframe.columns:
                dataframe[column] = ""

        dataframe = dataframe[self.columns]

        dataframe.fillna("", inplace=True)

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
        ).fillna(
            MONTHLY_OT_LIMIT_MINUTES
        ).astype(int)

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
            ) is not None
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

        return dataframe.loc[index].to_dict()

    # =====================================================
    # Get All Employees
    # =====================================================

    def get_all_employees(self):

        dataframe = self._get_dataframe()

        return dataframe.to_dict(
            orient="records"
        )

    # =====================================================
    # HH:MM -> Minutes
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
            "-",
            "None",
            "nan"
        ):
            return 0

        try:

            hours, minutes = map(
                int,
                value.split(":")
            )

            return (hours * 60) + minutes

        except Exception:

            return 0

    # =====================================================
    # Minutes -> HH:MM
    # =====================================================

    def minutes_to_time(
        self,
        minutes
    ):

        try:

            minutes = max(
                0,
                int(minutes)
            )

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

        # ------------------------------------------
        # Initialize Day1-Day31
        # ------------------------------------------

        for day in range(1, 32):

            record[f"Day{day}"] = "00:00"

        # ------------------------------------------
        # Monthly Details
        # ------------------------------------------

        record["Monthly OT"] = "00:00"

        record["Monthly OT Minutes"] = 0

        record["Remaining OT"] = self.minutes_to_time(
            MONTHLY_OT_LIMIT_MINUTES
        )

        record["Remaining OT Minutes"] = (
            MONTHLY_OT_LIMIT_MINUTES
        )

        record["Monthly Status"] = NORMAL_STATUS

        record["Last Updated"] = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        dataframe.loc[len(dataframe)] = record

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

        # ------------------------------------------
        # Create Employee if Not Exists
        # ------------------------------------------

        if index is None:

            index = self.create_employee(
                dataframe,
                employee
            )

        # ------------------------------------------
        # Update Basic Information
        # ------------------------------------------

        dataframe.at[index, "Employee Name"] = employee.get("name", "")
        dataframe.at[index, "Department"] = employee.get("department", "")
        dataframe.at[index, "Designation"] = employee.get("designation", "")
        dataframe.at[index, "Email"] = employee.get("email", "")
        dataframe.at[index, "Phone"] = employee.get("phone", "")

        # ------------------------------------------
        # Attendance Date
        # ------------------------------------------

        attendance_date = employee.get("attendance_date",datetime.now())
        
        if isinstance(attendance_date, str):
            
            attendance_date = pd.to_datetime(
                attendance_date,
                errors="coerce",
                dayfirst=True
            )

        if attendance_date is None or pd.isna(attendance_date):
            attendance_date = datetime.now()

        day = int(employee.get("current_day", attendance_date.day))
        if employee_id == "U1- 0005":
            print("=" * 60)
            print("Attendance Date :", attendance_date)
            print("Employee ID     :", employee_id)
            print("Saving Column   :", f"Day{day}")
            print("=" * 60)
        month = attendance_date.month
        year = attendance_date.year

        # ------------------------------------------
        # Monthly Reset (Only if Month Changed)
        # ------------------------------------------

        try:

            last_updated = str(
                dataframe.at[
                    index,
                    "Last Updated"
                ]
            )

            last_date = pd.to_datetime(
                last_updated,
                dayfirst=True,
                errors="coerce"
            )

            if (
                pd.notna(last_date)
                and
                (
                    last_date.month != month
                    or
                    last_date.year != year
                )
            ):

                for i in range(1, 32):

                    dataframe.at[
                        index,
                        f"Day{i}"
                    ] = "00:00"
            
                dataframe.at[index, "Monthly OT"] = "00:00"
                dataframe.at[index, "Monthly OT Minutes"] = 0
                dataframe.at[index, "Remaining OT"] = self.minutes_to_time(
                    MONTHLY_OT_LIMIT_MINUTES
                )
                dataframe.at[index, "Remaining OT Minutes"] = (
                    MONTHLY_OT_LIMIT_MINUTES
                )
                dataframe.at[index, "Monthly Status"] = NORMAL_STATUS

        except Exception:

            pass

        # ------------------------------------------
        # Save Today's OT
        # ------------------------------------------

        daily_ot = str(
            employee.get(
                "daily_ot",
                "00:00"
            )
        ).strip()

        if daily_ot in (
            "",
            "None",
            "nan"
        ):
            daily_ot = "00:00"

        column_name = f"Day{day}"
        
        old_value = str(dataframe.at[index, column_name]).strip()
        
        if old_value in ("","nan","None"):
            old_value = "00:00"
            
        dataframe.at[index, column_name] = daily_ot
        print(f"Day{day} Saved =", daily_ot)
        
        print("=" * 60)
        print("Employee ID :", employee_id)
        print("Attendance  :", attendance_date)
        print("Saved Into  :", f"Day{day}")
        print("Daily OT    :", daily_ot)
        print("=" * 60)
        # ------------------------------------------
        # Calculate Monthly OT
        # ------------------------------------------

        total_minutes = 0

        for i in range(1, 32):
            
            value = str(dataframe.at[index, f"Day{i}"]).strip()
            
            if value in ("","nan","None"):
                value = "00:00"
                
            total_minutes += self.time_to_minutes(value)
        
        monthly_ot = self.minutes_to_time(total_minutes)

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

        print(f"Remaining OT : {remaining_ot}")
        # ------------------------------------------
        # Monthly Status
        # ------------------------------------------

        if total_minutes > MONTHLY_OT_LIMIT_MINUTES:

            status = EXCEEDED_STATUS

        elif total_minutes == MONTHLY_OT_LIMIT_MINUTES:

            status = LIMIT_REACHED_STATUS

        elif total_minutes >= MONTHLY_OT_WARNING_MINUTES:

            status = WARNING_STATUS

        else:

            status = NORMAL_STATUS

        # ------------------------------------------
        # Update Database
        # ------------------------------------------

        dataframe.at[index, "Monthly OT"] = monthly_ot

        dataframe.at[index, "Monthly OT Minutes"] = (
            total_minutes
        )

        dataframe.at[index, "Remaining OT"] = (
            remaining_ot
        )

        dataframe.at[index, "Remaining OT Minutes"] = (
            remaining_minutes
        )

        dataframe.at[index, "Monthly Status"] = status

        dataframe.at[index, "Last Updated"] = attendance_date.strftime("%d-%b-%Y")

        # ------------------------------------------
        # Save Database
        # ------------------------------------------

        self.save_database(
            dataframe
        )
        
        print("\nSaved Database Successfully!")

        self._clear_cache()

        # ------------------------------------------
        # Reload Updated Employee
        # ------------------------------------------

        updated_employee = self.get_employee(
            employee_id
        )
        if updated_employee is not None:
        
            print("\nReloaded Database")
        
            for i in range(1, 32):
                day_value = updated_employee.get(
                    f"Day{i}",
                    "00:00"
                )

                print(
                    f"Day{i:02d} : "
                    f"{day_value}  "
                    f"({self.time_to_minutes(day_value)} mins)"
                )

            employee["monthly_ot"] = updated_employee.get(
                "Monthly OT",
                "00:00"
            )

            employee["monthly_ot_minutes"] = int(
                updated_employee.get(
                    "Monthly OT Minutes",
                    0
                )
            )

            employee["remaining_ot"] = updated_employee.get(
                "Remaining OT",
                "00:00"
            )

            employee["remaining_ot_minutes"] = int(
                updated_employee.get(
                    "Remaining OT Minutes",
                    MONTHLY_OT_LIMIT_MINUTES
                )
            )

            employee["monthly_status"] = updated_employee.get(
                "Monthly Status",
                NORMAL_STATUS
            )

            for i in range(1, 32):

                employee[f"Day{i}"] = updated_employee.get(
                    f"Day{i}",
                    "00:00"
                )

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
            "monthly_ot_exceeded": 0,
            "total_monthly_ot":"00:00"
        }

        if dataframe.empty:
            return summary

        summary["overtime"] = len(
            dataframe[
                dataframe["Monthly OT Minutes"] > 0
            ]
        )

        status_counts = dataframe[
            "Monthly Status"
        ].value_counts()

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
        
        total_inutes = dataframe["Monthly OT Minutes"].fillna(0).astype(int).sum()
        
        hours = total_inutes // 60
        minutes = total_inutes % 60
        
        summary["total_monthly_ot"] = f"{hours:02d}:{minutes:02d}"

        return summary


    # =====================================================
    # Monthly Reset
    # =====================================================

    def monthly_reset(self):

        dataframe = self._get_dataframe()

        if dataframe.empty:
            return False

        for day in range(1, 32):

            dataframe[f"Day{day}"] = "00:00"

        dataframe["Monthly OT"] = "00:00"

        dataframe["Monthly OT Minutes"] = 0

        dataframe["Remaining OT"] = self.minutes_to_time(
            MONTHLY_OT_LIMIT_MINUTES
        )

        dataframe["Remaining OT Minutes"] = (
            MONTHLY_OT_LIMIT_MINUTES
        )

        dataframe["Monthly Status"] = NORMAL_STATUS

        dataframe["Last Updated"] = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

        self.save_database(dataframe)

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
    # Finalize
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