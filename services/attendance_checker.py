"""
=========================================================
Attendance Notification System Pro
Attendance Checker
Version : 10.0 Enterprise
Developed by Maharajan
=========================================================
"""

import gc
import os
import time
from datetime import datetime

import pandas as pd

from config import (
    SHIFT_START,
    SHIFT_END,
    GRACE_TIME,
    CHECK_LATE_IN,
    CHECK_EARLY_OUT,
    CHECK_MISSING_IN,
    CHECK_MISSING_OUT
)

from services.database_manager import DatabaseManager
from services.overtime_checker import OvertimeManager
from services.hr_report import HRReportGenerator
from services.notification_service import NotificationService


class AttendanceChecker:
    """
    Enterprise Attendance Processing Engine

    Features
    --------
    • High Performance Attendance Processing
    • Automatic Daily OT
    • Monthly OT Tracking
    • HR Report Generation
    • Employee Notifications
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.shift_start = datetime.strptime(
            SHIFT_START,
            "%H:%M"
        )

        self.shift_end = datetime.strptime(
            SHIFT_END,
            "%H:%M"
        )

        self.grace_time = datetime.strptime(
            GRACE_TIME,
            "%H:%M"
        )

        # -----------------------------------------
        # Services
        # -----------------------------------------

        self.database = DatabaseManager()

        self.ot_manager = OvertimeManager(
            self.database
        )

        self.hr_generator = HRReportGenerator()

        self.notification_service = NotificationService()

        # -----------------------------------------
        # Required Attendance Columns
        # -----------------------------------------

        self.required_columns = [

            "Employee No",

            "Employee Name",

            "Attendance Date",

            "IN Time",

            "OUT Time"

        ]

        # -----------------------------------------
        # Empty Time Values
        # -----------------------------------------

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

        # -----------------------------------------
        # Supported Attendance Date Formats
        # -----------------------------------------

        self.date_formats = [

            "%d-%b-%Y",

            "%d-%B-%Y",

            "%d/%m/%Y",

            "%d-%m-%Y",

            "%Y-%m-%d"

        ]
        # =====================================================
    # Read Attendance File
    # =====================================================

    def read_file(
        self,
        filepath
    ):

        print("=" * 60)
        print("Reading Attendance File...")
        print("=" * 60)

        extension = os.path.splitext(
            filepath
        )[1].lower()

        # -----------------------------------------
        # Read CSV
        # -----------------------------------------

        if extension == ".csv":

            dataframe = None

            for encoding in (

                "utf-8",

                "utf-8-sig",

                "latin1",

                "cp1252"

            ):

                try:

                    dataframe = pd.read_csv(

                        filepath,

                        encoding=encoding,

                        low_memory=False

                    )

                    break

                except Exception:

                    continue

            if dataframe is None:

                raise ValueError(

                    "Unable to read CSV file."

                )

        # -----------------------------------------
        # Read Excel
        # -----------------------------------------

        elif extension in (

            ".xlsx",

            ".xls"

        ):

            dataframe = pd.read_excel(

                filepath,

                engine="openpyxl"

            )

        else:

            raise ValueError(

                f"Unsupported File : {extension}"

            )

        # -----------------------------------------
        # Clean Column Names
        # -----------------------------------------

        dataframe.columns = [

            str(column)

            .strip()

            .replace("\n", " ")

            .replace("\r", " ")

            for column in dataframe.columns

        ]

        dataframe.dropna(

            how="all",

            inplace=True

        )

        dataframe.reset_index(

            drop=True,

            inplace=True

        )

        # -----------------------------------------
        # Remove Empty Employee Rows
        # -----------------------------------------

        dataframe = dataframe.loc[

            dataframe["Employee No"]

            .notna()

        ]

        dataframe.reset_index(

            drop=True,

            inplace=True

        )

        print("=" * 60)
        print(

            f"Employees Found : {len(dataframe)}"

        )
        print("=" * 60)

        return dataframe
    # =====================================================
    # Convert Time
    # =====================================================

    def convert_time(
        self,
        value
    ):

        if value is None:
            return None

        if pd.isna(value):
            return None

        # -----------------------------------------
        # Excel Datetime
        # -----------------------------------------

        if isinstance(
            value,
            datetime
        ):
            return value

        # -----------------------------------------
        # Excel Float Time
        # -----------------------------------------

        if isinstance(
            value,
            (int, float)
        ):

            try:

                total_seconds = int(
                    float(value) * 86400
                )

                hours = (
                    total_seconds // 3600
                ) % 24

                minutes = (
                    total_seconds % 3600
                ) // 60

                return datetime.strptime(
                    f"{hours:02d}:{minutes:02d}",
                    "%H:%M"
                )

            except Exception:

                return None

        value = str(value).strip()

        if value in self.empty_time_values:
            return None

        value = (
            value
            .replace(".", ":")
            .replace("-", ":")
        )

        supported_formats = [

            "%H:%M",

            "%H:%M:%S",

            "%I:%M %p",

            "%I:%M:%S %p",

            "%I:%M%p",

            "%H.%M"

        ]

        for fmt in supported_formats:

            try:

                return datetime.strptime(
                    value,
                    fmt
                )

            except ValueError:

                continue

        return None


    # =====================================================
    # Format Time
    # =====================================================

    def format_time(
        self,
        value
    ):

        if value is None:

            return "--"

        if not isinstance(
            value,
            datetime
        ):

            return "--"

        return value.strftime(
            "%H:%M"
        )
        # =====================================================
    # Process Attendance File
    # =====================================================

    def process_excel(
        self,
        attendance_file
    ):

        start_time = time.perf_counter()

        print("=" * 60)
        print("Attendance Processing Started")
        print("=" * 60)

        dataframe = self.read_file(
            attendance_file
        )

        if dataframe.empty:

            raise ValueError(
                "Attendance file is empty."
            )

        # -----------------------------------------
        # Validate Required Columns
        # -----------------------------------------

        missing_columns = [

            column

            for column in self.required_columns

            if column not in dataframe.columns

        ]

        if missing_columns:

            raise ValueError(

                "Missing Required Columns : "

                + ", ".join(missing_columns)

            )

        employees = []

        summary = {

            "total": 0,

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

        for _, row in dataframe.iterrows():

            summary["total"] += 1

            # -----------------------------------------
            # Attendance Date
            # -----------------------------------------

            attendance_date = str(

                row.get(

                    "Attendance Date",

                    ""

                )

            ).strip()

            for fmt in self.date_formats:

                try:

                    attendance_date = datetime.strptime(

                        attendance_date,

                        fmt

                    ).strftime("%Y-%m-%d")

                    break

                except Exception:

                    continue

            # -----------------------------------------
            # Employee Information
            # -----------------------------------------

            employee = {

                "employee_id": str(

                    row.get(

                        "Employee No",

                        ""

                    )

                ).strip(),

                "name": str(

                    row.get(

                        "Employee Name",

                        ""

                    )

                ).strip(),

                "department": str(

                    row.get(

                        "Department",

                        ""

                    )

                ).strip(),

                "designation": str(

                    row.get(

                        "Designation",

                        ""

                    )

                ).strip(),

                "attendance_date": attendance_date,

                "email": str(

                    row.get(

                        "Email",

                        ""

                    )

                ).strip(),

                "status": []

            }

            # -----------------------------------------
            # Punch Times
            # -----------------------------------------

            in_time = self.convert_time(

                row.get(

                    "IN Time"

                )

            )

            out_time = self.convert_time(

                row.get(

                    "OUT Time"

                )

            )

            employee["punch_in"] = self.format_time(
                in_time
            )

            employee["punch_out"] = self.format_time(
                out_time
            )

            # -----------------------------------------
            # Late / Early
            # -----------------------------------------

            late = str(

                row.get(

                    "Late IN(HH:MM)",

                    row.get(

                        "Late IN",

                        "00:00"

                    )

                )

            ).strip()

            early = str(

                row.get(

                    "Early OUT(HH:MM)",

                    row.get(

                        "Early OUT",

                        "00:00"

                    )

                )

            ).strip()

            # -----------------------------------------
            # Daily OT
            # -----------------------------------------

            daily_ot = str(

                row.get(

                    "OT HRS",

                    row.get(

                        "OT",

                        "0.00"

                    )

                )

            ).strip()

            if "." in daily_ot:

                try:

                    hour, minute = daily_ot.split(".")

                    daily_ot = (

                        f"{int(hour):02d}:"

                        f"{int(minute):02d}"

                    )

                except Exception:

                    daily_ot = "00:00"

            elif ":" not in daily_ot:

                daily_ot = "00:00"

            employee["daily_ot"] = daily_ot

            # -----------------------------------------
            # Convert Daily OT to Minutes
            # -----------------------------------------

            if ":" in daily_ot:

                hours, minutes = daily_ot.split(":")

                employee["daily_ot_minutes"] = (
                    int(hours) * 60 + int(minutes)
                )

            else:

                employee["daily_ot_minutes"] = 0
            # =====================================================
            # Attendance Validation
            # =====================================================

            status = employee["status"]

            # -----------------------------------------
            # Missing Punch In
            # -----------------------------------------

            if CHECK_MISSING_IN and in_time is None:

                status.append(
                    "Missing Punch In"
                )

                summary["missing_in"] += 1

            # -----------------------------------------
            # Missing Punch Out
            # -----------------------------------------

            if CHECK_MISSING_OUT and out_time is None:

                status.append(
                    "Missing Punch Out"
                )

                summary["missing_out"] += 1

            # -----------------------------------------
            # Late Punch
            # -----------------------------------------

            if (
                CHECK_LATE_IN
                and late not in self.empty_time_values
                and late != "00:00"
            ):

                status.append(
                    f"Late Punch ({late})"
                )

                summary["late_in"] += 1

            # -----------------------------------------
            # Early Out
            # -----------------------------------------

            if (
                CHECK_EARLY_OUT
                and early not in self.empty_time_values
                and early != "00:00"
            ):

                status.append(
                    f"Early Out ({early})"
                )

                summary["early_out"] += 1

            # =====================================================
            # Overtime Processing
            # =====================================================

            employee = self.ot_manager.process(
                employee,
                out_time
            )
            # -----------------------------------------
            # Preserve uploaded Daily OT
            # -----------------------------------------

            employee["daily_ot"] = daily_ot

            if ":" in daily_ot:

                hours, minutes = daily_ot.split(":")

                employee["daily_ot_minutes"] = (
                    int(hours) * 60 + int(minutes)
                )

            else:

                employee["daily_ot_minutes"] = 0

            # -----------------------------------------
            # Daily OT Employee
            # -----------------------------------------

            if employee.get(
                "daily_ot_minutes",
                0
            ) > 0:

                status.append(
                    f"Daily OT ({employee['daily_ot']})"
                )

                summary["overtime"] += 1

            # -----------------------------------------
            # Monthly Status
            # -----------------------------------------

            monthly_status = employee.get(
                "monthly_status",
                "Normal"
            )

            if monthly_status == "Warning":

                summary["monthly_warning"] += 1

                status.append(
                    "Monthly OT Warning"
                )

            elif monthly_status == "Limit Reached":

                summary["monthly_limit_reached"] += 1

                status.append(
                    "Monthly OT Limit Reached"
                )

            elif monthly_status == "Exceeded":

                summary["monthly_ot_exceeded"] += 1

                status.append(
                    "Monthly OT Exceeded"
                )

            # =====================================================
            # Present Count
            # =====================================================

            attendance_issue = False

            for item in status:

                if (

                    "Late Punch" in item

                    or

                    "Early Out" in item

                    or

                    "Missing Punch" in item

                ):

                    attendance_issue = True

                    break

            if not attendance_issue:

                summary["present"] += 1

            # -----------------------------------------
            # On Time
            # -----------------------------------------

            if len(status) == 0:

                status.append(
                    "On Time"
                )

            # =====================================================
            # Generate Notification
            # =====================================================

            employee["notification"] = (

                self.notification_service.generate_message(
                    employee
                )

            )

            employees.append(
                employee
            )
            # =====================================================
        # Save Monthly OT Database
        # =====================================================

        print("=" * 60)
        print("Saving Monthly OT Database...")
        print("=" * 60)

        self.database.finalize()

        print("=" * 60)
        print("Monthly OT Database Saved Successfully")
        print("=" * 60)

        # =====================================================
        # Generate HR Reports
        # =====================================================

        reports = self.hr_generator.generate(
            employees,
            summary
        )

        hr_report = reports.get(
            "hr_report",
            ""
        )

        late_punch_report = reports.get(
            "late_punch_report",
            ""
        )

        # =====================================================
        # Top Monthly OT Employees
        # =====================================================

        top_ot_employees = sorted(

            employees,

            key=lambda employee: employee.get(
                "monthly_ot_minutes",
                0
            ),

            reverse=True

        )[:10]

        # =====================================================
        # Dashboard Statistics
        # =====================================================

        attendance_statistics = {

            "present": summary["present"],

            "late": summary["late_in"],

            "early": summary["early_out"],

            "missing_in": summary["missing_in"],

            "missing_out": summary["missing_out"]

        }

        monthly_ot_statistics = {

            "warning": summary["monthly_warning"],

            "limit_reached": summary["monthly_limit_reached"],

            "exceeded": summary["monthly_ot_exceeded"]

        }

        # =====================================================
        # Processing Time
        # =====================================================

        processing_time = round(

            time.perf_counter() - start_time,

            2

        )

        print("=" * 60)
        print(
            f"Processing Time : {processing_time} Seconds"
        )
        print("=" * 60)

        print("=" * 60)
        print("Attendance Processing Completed Successfully")
        print("=" * 60)

        # =====================================================
        # Dashboard Result
        # =====================================================

        result = {

            "summary": {

                "total": summary["total"],

                "present": summary["present"],

                "late_in": summary["late_in"],

                "early_out": summary["early_out"],

                "missing_in": summary["missing_in"],

                "missing_out": summary["missing_out"],

                "overtime": summary["overtime"],

                "monthly_warning": summary["monthly_warning"],

                "monthly_limit_reached": summary["monthly_limit_reached"],

                "monthly_ot_exceeded": summary["monthly_ot_exceeded"]

            },

            "attendance_statistics": attendance_statistics,

            "monthly_ot_statistics": monthly_ot_statistics,

            "top_ot_employees": top_ot_employees,

            "employees": self.group_dashboard_data(employees),

            "hr_report": hr_report,

            "late_punch_report": late_punch_report,

            "processing_time": processing_time

        }
        

        # =====================================================
        # Cleanup
        # =====================================================

        del dataframe

        gc.collect()

        return result


    # =====================================================
    # Dashboard Employee Grouping
    # =====================================================
    def group_dashboard_data(self, employees):

        grouped = {}

        for emp in employees:

            emp_id = (
                str(emp["employee_id"])
                .replace(".0","")
                .strip()
                .upper()
            )
            print("Grouping ID:",repr(emp_id))

            if emp_id not in grouped:

                grouped[emp_id] = {
                    "employee_id": emp["employee_id"],
                    "name": emp["name"],
                    "department": emp.get("department", ""),
                    "designation": emp.get("designation", ""),
                    "monthly_ot": emp.get("monthly_ot", "00:00"),
                    "remaining_ot": emp.get("remaining_ot", "00:00"),
                    "monthly_status": emp.get("monthly_status", "Normal"),
                    "daily_data": []
                }

            grouped[emp_id]["daily_data"].append({
                "date": emp["attendance_date"],
                "punch_in": emp["punch_in"],
                "punch_out": emp["punch_out"],
                "daily_ot": emp["daily_ot"]
            })
            
        print("=" * 60)
        print("Original Employees:",len(employees))
        print("Grouped Employees:",len(grouped))
        print("=" * 60)

        return list(grouped.values())