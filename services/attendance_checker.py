"""
=========================================================
Attendance Notification System Pro
Attendance Checker
Version : 8.0 Enterprise (Ultra Performance)
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
    • High-performance attendance processing
    • Single database load/save
    • Optimized for large Excel/CSV files
    • Low memory usage
    • HR report generation
    • Employee notification generation
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

        # ---------------------------------------------
        # Shared Services
        # ---------------------------------------------

        self.database = DatabaseManager()

        self.ot_manager = OvertimeManager(
            self.database
        )

        self.hr_generator = HRReportGenerator()

        self.notification_service = NotificationService()

        # ---------------------------------------------
        # Required Columns
        # ---------------------------------------------

        self.required_columns = (

            "Employee No",

            "Employee Name",

            "Attendance Date",

            "IN Time",

            "OUT Time"

        )

        # ---------------------------------------------
        # Invalid Time Values
        # ---------------------------------------------

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

        if extension == ".csv":

            try:

                dataframe = pd.read_csv(
                    filepath,
                    encoding="utf-8",
                    low_memory=False
                )

            except UnicodeDecodeError:

                dataframe = pd.read_csv(
                    filepath,
                    encoding="latin1",
                    low_memory=False
                )

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
                f"Unsupported file format : {extension}"
            )

        dataframe.columns = [

            str(column).strip()

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

        if isinstance(
            value,
            datetime
        ):

            return value

        value = str(value).strip()

        if value in self.empty_time_values:

            return None

        value = (
            value
            .replace(".", ":")
            .replace("-", ":")
        )

        for fmt in (

            "%H:%M",

            "%H:%M:%S",

            "%I:%M %p",

            "%I:%M:%S %p",

            "%I:%M%p"

        ):

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
            "%I:%M %p"
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

        # =====================================================
        # Required Columns
        # =====================================================

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

        print("Required Columns Verified")

        # =====================================================
        # Initialize
        # =====================================================

        employees = []

        summary = {

            "total": 0,

            "present": 0,

            "late_in": 0,

            "early_out": 0,

            "missing_in": 0,

            "missing_out": 0,

            "overtime": 0,

            "warning": 0,

            "limit_reached": 0,

            "monthly_ot_exceeded": 0

        }

        total_rows = len(dataframe)

        print("=" * 60)
        print(
            f"Employees Found : {total_rows}"
        )
        print("=" * 60)

        # =====================================================
        # Performance Cache
        # =====================================================

        convert_time = self.convert_time

        format_time = self.format_time

        process_ot = self.ot_manager.process

        generate_notification = (

            self.notification_service.generate_message

        )

        employees_append = employees.append

        empty_time_values = self.empty_time_values

        # =====================================================
        # Process Employees
        # =====================================================

        for index, row in enumerate(

            dataframe.itertuples(index=False),

            start=1

        ):

            if index % 250 == 0 or index == total_rows:

                progress = round(

                    (index / total_rows) * 100,

                    1

                )

                print(

                    f"Processed {index}/{total_rows} ({progress}%)"

                )

            summary["total"] += 1

            # =====================================================
            # Employee Information
            # =====================================================

            employee = {

                "employee_id": str(
                    getattr(
                        row,
                        "Employee_No",
                        ""
                    )
                ).strip(),

                "name": str(
                    getattr(
                        row,
                        "Employee_Name",
                        ""
                    )
                ).strip(),

                "unit": str(
                    getattr(
                        row,
                        "Unit",
                        ""
                    )
                ).strip(),

                "department": str(
                    getattr(
                        row,
                        "Department",
                        ""
                    )
                ).strip(),

                "designation": str(
                    getattr(
                        row,
                        "Designation",
                        ""
                    )
                ).strip(),

                "attendance_date": str(
                    getattr(
                        row,
                        "Attendance_Date",
                        ""
                    )
                ).strip(),

                "approval_status": str(
                    getattr(
                        row,
                        "Approval_Status",
                        ""
                    )
                ).strip(),

                "remarks": str(
                    getattr(
                        row,
                        "Remarks",
                        ""
                    )
                ).strip(),

                "email": str(
                    getattr(
                        row,
                        "Email",
                        ""
                    )
                ).strip(),

                "status": [],

                "notification": ""

            }

            status = employee["status"]

            status_append = status.append

            # =====================================================
            # Punch Details
            # =====================================================

            in_time = convert_time(

                getattr(
                    row,
                    "IN_Time",
                    ""
                )

            )

            out_time = convert_time(

                getattr(
                    row,
                    "OUT_Time",
                    ""
                )

            )

            employee["punch_in"] = format_time(
                in_time
            )

            employee["punch_out"] = format_time(
                out_time
            )

            late = str(

                getattr(
                    row,
                    "Late_IN_HH_MM",
                    ""
                )

            ).strip()

            early = str(

                getattr(
                    row,
                    "Early_OUT_HH_MM",
                    ""
                )

            ).strip()

            employee["daily_ot"] = str(

                getattr(
                    row,
                    "OT_HRS",
                    "00:00"

                )

            ).strip()
            # =====================================================
            # Attendance Validation
            # =====================================================

            if CHECK_MISSING_IN and in_time is None:

                status_append(
                    "Missing Punch In"
                )

                summary["missing_in"] += 1

            if CHECK_MISSING_OUT and out_time is None:

                status_append(
                    "Missing Punch Out"
                )

                summary["missing_out"] += 1

            if (

                CHECK_LATE_IN

                and late not in empty_time_values

            ):

                status_append(

                    f"Late Punch ({late})"

                )

                summary["late_in"] += 1

            if (

                CHECK_EARLY_OUT

                and early not in empty_time_values

            ):

                status_append(

                    f"Early Out ({early})"

                )

                summary["early_out"] += 1

            # =====================================================
            # Overtime Processing
            # =====================================================

            employee = process_ot(

                employee,

                out_time

            )
            print("=" * 60)
            print(employee["employee_id"])
            print("Daily OT :", employee.get("daily_ot"))
            print("Monthly OT :", employee.get("monthly_ot"))
            print("Remaining OT :", employee.get("remaining_ot"))
            print("=" * 60)

            if employee.get(

                "daily_ot_minutes",

                0

            ) > 0:

                status_append(

                    f"Daily OT ({employee['daily_ot']})"

                )

                summary["overtime"] += 1

            monthly_status = employee.get(

                "monthly_status",

                "Normal"

            )

            if monthly_status == "Warning":

                status_append(

                    "Monthly OT Warning"

                )

                summary["warning"] += 1

            elif monthly_status == "Limit Reached":

                status_append(

                    "Monthly OT Limit Reached"

                )

                summary["limit_reached"] += 1

            elif monthly_status == "Exceeded":

                status_append(

                    "Monthly OT Exceeded"

                )

                summary["monthly_ot_exceeded"] += 1

            # =====================================================
            # Present Employee
            # =====================================================

            if not status:

                status_append(

                    "On Time"

                )

                summary["present"] += 1

            # =====================================================
            # Generate Notification
            # =====================================================

            employee["notification"] = (

                generate_notification(

                    employee

                )

            )

            # =====================================================
            # Store Employee
            # =====================================================

            employees_append(

                employee

            )
            # =====================================================
        # Finalize Database
        # =====================================================

        print("=" * 60)
        print("Saving Monthly OT Database...")
        print("=" * 60)

        self.database.finalize()

        print("=" * 60)
        print("Database Saved Successfully")
        print("=" * 60)

        # =====================================================
        # Generate HR Report
        # =====================================================

        print("=" * 60)
        print("Generating HR Report...")
        print("=" * 60)

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

        print("=" * 60)
        print("HR Report Generated Successfully")
        print("=" * 60)

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

        # =====================================================
        # Attendance Processing Completed
        # =====================================================

        print("=" * 60)
        print("Attendance Processing Completed Successfully")
        print("=" * 60)

        # =====================================================
        # Return Result
        # =====================================================

        result = {

            "summary": summary,

            "employees": employees,

            "hr_report": hr_report,

            "late_punch_report": late_punch_report,

            "processing_time": processing_time

        }

        # =====================================================
        # Memory Cleanup
        # =====================================================

        gc.collect()

        return result