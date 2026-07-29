"""
=========================================================
Attendance Notification System Pro
Enterprise Attendance Checker
Version : 13.0 Enterprise
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
    CHECK_MISSING_OUT,
    EMPLOYEE_ID_COLUMNS,
    EMPLOYEE_NAME_COLUMNS,
    DATE_COLUMNS,
    IN_TIME_COLUMNS,
    OUT_TIME_COLUMNS,
    OT_COLUMNS,
    LATE_COLUMNS,
    EARLY_COLUMNS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS,
    NORMAL_STATUS,
)

from services.database_manager import DatabaseManager
from services.overtime_manager import OvertimeManager
from services.notification_service import NotificationService
from services.hr_report import HRReportGenerator


class AttendanceChecker:

    """
    Enterprise Attendance Processing Engine
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.database = DatabaseManager()

        self.overtime = OvertimeManager()

        self.notification = NotificationService()

        self.hr_report = HRReportGenerator()

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

        self.empty_values = {
            "",
            "-",
            "--",
            "0",
            "0.0",
            "00:00",
            "00:00:00",
            "nan",
            "NaN",
            None
        }

        self.time_formats = [
            "%H:%M",
            "%H:%M:%S",
            "%I:%M %p",
            "%I:%M:%S %p",
            "%I:%M%p"
        ]
        # =====================================================
    # Read Attendance File
    # =====================================================

    def read_file(self, filepath):

        extension = os.path.splitext(filepath)[1].lower()

        # -----------------------------------------
        # CSV
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
                raise Exception(
                    "Unable to read CSV file."
                )

        # -----------------------------------------
        # Excel
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

            raise Exception(
                f"Unsupported File : {extension}"
            )

        # -----------------------------------------
        # Clean Columns
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

        return dataframe

    # =====================================================
    # Find Column
    # =====================================================

    def find_column(
        self,
        dataframe,
        aliases
    ):

        columns = {

            str(column).lower().strip(): column

            for column in dataframe.columns

        }

        for alias in aliases:

            if alias.lower() in columns:

                return columns[alias.lower()]

        return None

    # =====================================================
    # Detect Columns
    # =====================================================

    def detect_columns(
        self,
        dataframe
    ):

        detected = {

            "employee_id": self.find_column(
                dataframe,
                EMPLOYEE_ID_COLUMNS
            ),

            "employee_name": self.find_column(
                dataframe,
                EMPLOYEE_NAME_COLUMNS
            ),

            "attendance_date": self.find_column(
                dataframe,
                DATE_COLUMNS
            ),

            "in_time": self.find_column(
                dataframe,
                IN_TIME_COLUMNS
            ),

            "out_time": self.find_column(
                dataframe,
                OUT_TIME_COLUMNS
            ),

            "ot": self.find_column(
                dataframe,
                OT_COLUMNS
            ),

            "late": self.find_column(
                dataframe,
                LATE_COLUMNS
            ),

            "early": self.find_column(
                dataframe,
                EARLY_COLUMNS
            )

        }

        required = [

            "employee_id",
            "employee_name",
            "attendance_date",
            "in_time",
            "out_time"

        ]

        missing = [

            column

            for column in required

            if detected[column] is None

        ]

        if missing:

            raise Exception(

                "Missing Required Columns : "

                + ", ".join(missing)

            )

        return detected
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

        if isinstance(value, datetime):
            return value

        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()

        # -----------------------------------------
        # Excel Float Time
        # -----------------------------------------

        if isinstance(value, (int, float)):

            try:

                if value >= 1:
                    value = value % 1

                total_seconds = int(round(value * 86400))

                hours = total_seconds // 3600

                minutes = (total_seconds % 3600) // 60

                return datetime.strptime(
                    f"{hours:02d}:{minutes:02d}",
                    "%H:%M"
                )

            except Exception:

                return None

        value = str(value).strip()

        if value in self.empty_values:
            return None

        value = (
            value.replace(".", ":")
                 .replace("-", ":")
        )

        for fmt in self.time_formats:

            try:

                return datetime.strptime(
                    value,
                    fmt
                )

            except Exception:

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

        if not isinstance(value, datetime):
            return "--"

        return value.strftime("%H:%M")

    # =====================================================
    # Read Daily OT
    # =====================================================

    def read_ot(
        self,
        value
    ):

        if value is None:
            return "00:00"

        if pd.isna(value):
            return "00:00"

        value = str(value).strip()

        if value in self.empty_values:
            return "00:00"

        # HH:MM format
        if ":" in value:

            try:

                hours, minutes = value.split(":")

                return f"{int(hours):02d}:{int(minutes):02d}"

            except Exception:

                return "00:00"

        # Decimal format (Example: 1.30)
        if "." in value:

            try:

                parts = value.split(".")

                if len(parts) == 2:

                    hours = int(parts[0])
                    minutes = int(parts[1])

                    if minutes > 59:
                        minutes = 59

                    return f"{hours:02d}:{minutes:02d}"

            except Exception:
                pass

        # Hours only
        try:

            hours = int(float(value))

            return f"{hours:02d}:00"

        except Exception:

            return "00:00"
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

        # -----------------------------------------
        # Read Attendance File
        # -----------------------------------------

        dataframe = self.read_file(
            attendance_file
        )

        if dataframe.empty:

            raise Exception(
                "Attendance file is empty."
            )

        # -----------------------------------------
        # Detect Columns
        # -----------------------------------------

        columns = self.detect_columns(
            dataframe
        )

        # -----------------------------------------
        # Initialize Employee List
        # -----------------------------------------

        employees = []

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        summary = {

            "total": 0,

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

        print("=" * 60)
        print("Columns Detected")
        print("=" * 60)

        for key, value in columns.items():

            print(f"{key:<20}: {value}")

        print("=" * 60)

        # -----------------------------------------
        # Process Employees
        # -----------------------------------------

        for _, row in dataframe.iterrows():

            summary["total"] += 1

            employee = {

                "employee_id": str(
                    row.get(
                        columns["employee_id"],
                        ""
                    )
                ).strip(),

                "name": str(
                    row.get(
                        columns["employee_name"],
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

                "email": str(
                    row.get(
                        "Email",
                        ""
                    )
                ).strip(),

                "phone": str(
                    row.get(
                        "Phone",
                        ""
                    )
                ).strip(),

                "attendance_date": "",

                "punch_in": "--",

                "punch_out": "--",

                "daily_ot": "00:00",

                "daily_ot_minutes": 0,

                "monthly_ot": "00:00",

                "monthly_ot_minutes": 0,

                "remaining_ot": "25:00",

                "remaining_ot_minutes": 1500,

                "daily_status": NORMAL_STATUS,

                "monthly_status": NORMAL_STATUS,

                "status": [],

                "notification": ""

            }
            # =====================================================
            # Attendance Date
            # =====================================================

            attendance_date = row.get(
                columns["attendance_date"]
            )

            day = 1

            if pd.notna(attendance_date):

                try:

                    attendance_date = pd.to_datetime(
                        attendance_date
                    )

                    employee["attendance_date"] = (
                        attendance_date.strftime("%d-%m-%Y")
                    )

                    day = attendance_date.day

                except Exception:

                    employee["attendance_date"] = str(
                        attendance_date
                    )

            # =====================================================
            # Punch In / Punch Out
            # =====================================================

            in_time = self.convert_time(

                row.get(
                    columns["in_time"]
                )

            )

            out_time = self.convert_time(

                row.get(
                    columns["out_time"]
                )

            )

            employee["punch_in"] = self.format_time(
                in_time
            )

            employee["punch_out"] = self.format_time(
                out_time
            )

            # =====================================================
            # Daily OT
            # =====================================================

            if columns["ot"] is not None:

                employee["daily_ot"] = self.read_ot(

                    row.get(
                        columns["ot"]
                    )

                )

            else:

                employee["daily_ot"] = "00:00"

            # Convert Daily OT to Minutes

            hh, mm = employee["daily_ot"].split(":")

            employee["daily_ot_minutes"] = (

                int(hh) * 60 +

                int(mm)

            )

            # =====================================================
            # Attendance Status
            # =====================================================

            attendance = str(

                row.get(
                    "Attendance Status",
                    ""
                )

            ).strip().upper()

            if attendance == "P/P":

                summary["present"] += 1

                employee["daily_status"] = "Present"

            elif attendance == "A/A":

                summary["absent"] += 1

                employee["daily_status"] = "Absent"

                employee["status"].append("Absent")

            elif attendance == "P/A":

                summary["half_day"] += 1

                employee["daily_status"] = "Half Day"

                employee["status"].append("Half Day")

            else:

                employee["daily_status"] = "Unknown"
                # =====================================================
            # Late Punch
            # =====================================================

            if columns["late"] is not None:

                late = str(

                    row.get(
                        columns["late"],
                        "00:00"
                    )

                ).strip()

                if (

                    CHECK_LATE_IN

                    and late not in self.empty_values

                    and late != "00:00"

                ):

                    summary["late_in"] += 1

                    employee["status"].append(

                        f"Late Punch ({late})"

                    )

            # =====================================================
            # Early Out
            # =====================================================

            if columns["early"] is not None:

                early = str(

                    row.get(
                        columns["early"],
                        "00:00"
                    )

                ).strip()

                if (

                    CHECK_EARLY_OUT

                    and early not in self.empty_values

                    and early != "00:00"

                ):

                    summary["early_out"] += 1

                    employee["status"].append(

                        f"Early Out ({early})"

                    )

            # =====================================================
            # Missing Punch In
            # =====================================================

            if CHECK_MISSING_IN and in_time is None:

                summary["missing_in"] += 1

                employee["status"].append(

                    "Missing Punch In"

                )

            # =====================================================
            # Missing Punch Out
            # =====================================================

            if CHECK_MISSING_OUT and out_time is None:

                summary["missing_out"] += 1

                employee["status"].append(

                    "Missing Punch Out"

                )

            # =====================================================
            # Overtime Processing
            # =====================================================

            employee = self.overtime.process(

                employee,

                out_time,

                day

            )

            # Preserve imported Daily OT if available

            if (

                employee["daily_ot"] == "00:00"

                and columns["ot"] is not None

            ):

                employee["daily_ot"] = self.read_ot(

                    row.get(
                        columns["ot"]
                    )

                )

            # =====================================================
            # Daily OT Summary
            # =====================================================

            if employee["daily_ot"] != "00:00":

                summary["overtime"] += 1

                employee["status"].append(

                    f"Daily OT ({employee['daily_ot']})"

                )

            # =====================================================
            # Monthly Status
            # =====================================================

            monthly_status = employee.get(

                "monthly_status",

                NORMAL_STATUS

            )

            if monthly_status == WARNING_STATUS:

                summary["monthly_warning"] += 1

            elif monthly_status == LIMIT_REACHED_STATUS:

                summary["monthly_limit_reached"] += 1

            elif monthly_status == EXCEEDED_STATUS:

                summary["monthly_ot_exceeded"] += 1

            # =====================================================
            # Default Status
            # =====================================================

            if len(employee["status"]) == 0:

                employee["status"].append(

                    "On Time"

                )

            # =====================================================
            # Notification
            # =====================================================

            employee["notification"] = (

                self.notification.generate_message(

                    employee

                )

            )
            # =====================================================
        # Save Employee
        # =====================================================

            employees.append(employee)

        # =====================================================
        # Save Monthly OT Database
        # =====================================================

        print("=" * 60)
        print("Saving Monthly OT Database...")
        print("=" * 60)

        for index, employee in enumerate(employees):

            employee[index] = self.database.update_employee(
                employee
            )

        self.database.finalize()
        
        for employee in employees:
            
            db_employee = self.database.get_employee(
                employee["employee_id"]    
            )
            
            if db_employee:
                
                employee["monthly_ot"] = db_employee.get(
                    "Monthly OT",
                    "00:00"
                )
                
                employee["monthly_ot_minutes"] = int(db_employee.get(
                    "Monthly OT Minutes",
                    0
                    )
                )
                
                employee["remaining_ot"] = db_employee.get(
                    "Remaining OT",
                    "25:00"
                )
                
                employee["remaining_ot_minutes"] = int(db_employee.get(
                    "Remaining OT Minutes",
                    1500
                    )
                )
                
                employee["monthly_status"] = db_employee.get(
                    "Monthly Status",
                    "Normal"
                    )
                
                for day in range(1,32):
                    employee[f"Day{day}"] = db_employee.get(
                        f"Day{day}",
                        "00:00"
                    )
                
            else:
                
                employee["monthly_ot"] = "00:00"
                employee ["monthly_ot_miutes"]= 0
                employee["remaing_ot"] = "25:00"
                employee["remaininig_ot_minutes"] = 1500
                employee["monthly_status"] ="Normal"
                
                for day in range(1,32):
                    employee[f"Day{day}"] = "00:00"

        print("=" * 60)
        print("Monthly OT Database Updated Successfully")
        print("=" * 60)

        # =====================================================
        # Dashboard Summary
        # =====================================================

        dashboard = self.database.get_dashboard_summary()

        # =====================================================
        # HR Report
        # =====================================================

        reports = self.hr_report.generate(
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

        top_ot = sorted(

            employees,

            key=lambda employee: employee.get(
                "monthly_ot_minutes",
                0
            ),

            reverse=True

        )[:10]

        # =====================================================
        # Processing Time
        # =====================================================

        processing_time = round(

            time.perf_counter() - start_time,

            2

        )

        print("=" * 60)
        print("Attendance Processing Completed")
        print("=" * 60)
        print(f"Processed Employees : {summary['total']}")
        print(f"Present             : {summary['present']}")
        print(f"Absent              : {summary['absent']}")
        print(f"Half Day            : {summary['half_day']}")
        print(f"Late Punch          : {summary['late_in']}")
        print(f"Early Out           : {summary['early_out']}")
        print(f"Missing Punch In    : {summary['missing_in']}")
        print(f"Missing Punch Out   : {summary['missing_out']}")
        print(f"Overtime            : {summary['overtime']}")
        print(f"Completed In        : {processing_time} Seconds")
        print("=" * 60)

        gc.collect()

        return {

            "employees": employees,

            "summary": summary,

            "dashboard": dashboard,

            "top_ot": top_ot,

            "processing_time": processing_time,

            "hr_report": hr_report,

            "late_punch_report": late_punch_report

        }