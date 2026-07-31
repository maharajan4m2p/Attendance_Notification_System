"""
=========================================================
Attendance Notification System Pro
Enterprise Attendance Checker
Version : 16.0 Enterprise
=========================================================
"""

import gc
import os
import time
from datetime import datetime
from typing import Any

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
    Version 16.0 Enterprise
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
            None,
        }

        self.time_formats = [

            "%H:%M",

            "%H:%M:%S",

            "%I:%M %p",

            "%I:%M:%S %p",

            "%I:%M%p",

        ]
        # =====================================================
        # Read Attendance File
        # =====================================================

    def read_file(self, filepath):

        extension = os.path.splitext(filepath)[1].lower()

        dataframe = None

        if extension == ".csv":

            encodings = [
                "utf-8",
                "utf-8-sig",
                "cp1252",
                "latin1",
            ]

            last_error = None

            for encoding in encodings:

                try:

                    dataframe = pd.read_csv(
                        filepath,
                        encoding=encoding,
                        low_memory=False
                    )

                    break

                except Exception as error:

                    last_error = error

            if dataframe is None:

                raise Exception(
                    f"Unable to read CSV file.\n{last_error}"
                )

        elif extension in [".xlsx", ".xls"]:

            dataframe = pd.read_excel(
                filepath,
                engine="openpyxl"
            )

        else:

            raise Exception(
                f"Unsupported File : {extension}"
            )

        dataframe.columns = [

            str(column)
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()

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

        available_columns = {

            str(column).strip().lower(): column

            for column in dataframe.columns

        }

        for alias in aliases:

            alias = alias.strip().lower()

            if alias in available_columns:

                return available_columns[alias]

        return None
    # =====================================================
    # Detect Required Columns
    # =====================================================

    def detect_columns(
        self,
        dataframe
    ):

        columns = {

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

            item

            for item in required

            if columns[item] is None

        ]

        if missing:

            raise Exception(

                "Missing Required Columns : "

                + ", ".join(missing)

            )

        print("=" * 60)
        print("Detected Columns")
        print("=" * 60)

        for key, value in columns.items():

            print(f"{key:<20}: {value}")

        print("=" * 60)

        return columns
    # =====================================================
    # Convert Time
    # =====================================================

    def convert_time(self, value):

        if value is None:
            return None

        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()

        if isinstance(value, (int, float)):

            try:

                if value >= 1:
                    value = value % 1

                total_seconds = round(value * 86400)

                hours = (total_seconds // 3600) % 24
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
                return datetime.strptime(value, fmt)

            except Exception:
                pass

        return None
    # =====================================================
    # Format Time
    # =====================================================

    def format_time(self, value):

        if value is None:
            return "--"

        if not isinstance(value, datetime):
            return "--"

        return value.strftime("%H:%M")
    # =====================================================
    # Read OT
    # =====================================================

    def read_ot(self, value):

        if value is None:
            return "00:00"

        if pd.isna(value):
            return "00:00"

        value = str(value).strip()

        if value in self.empty_values:
            return "00:00"

        try:

            value = value.replace(".", ":")

            if ":" in value:

                hh, mm = value.split(":")

                hh = max(0, int(hh))
                mm = max(0, min(59, int(mm)))

                return f"{hh:02d}:{mm:02d}"

            hh = int(float(value))

            return f"{hh:02d}:00"

        except Exception:

            return "00:00"
        # =====================================================
        # Process Attendance File
        # =====================================================

    def process_excel(self, attendance_file):

        start_time = time.perf_counter()

        print("=" * 60)
        print("Attendance Processing Started")
        print("=" * 60)

        # -----------------------------------------
        # Read Attendance File
        # -----------------------------------------

        dataframe = self.read_file(attendance_file)

        if dataframe.empty:
            raise Exception("Attendance file is empty.")

        # -----------------------------------------
        # Detect Required Columns
        # -----------------------------------------

        columns = self.detect_columns(dataframe)

        employees = []

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        summary: dict[str, Any] = {

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

            "monthly_ot_exceeded": 0,

        }

        print("=" * 60)
        print("Detected Columns")
        print("=" * 60)

        for key, value in columns.items():

            print(f"{key:<20}: {value}")

        print("=" * 60)

        # -----------------------------------------
        # Process Employees
        # -----------------------------------------

        for _, row in dataframe.iterrows():

            summary["total"] += 1
        # =====================================================
        # Employee Information
        # =====================================================

            employee = {

                "employee_id": str(
                    row.get(columns["employee_id"], "")
                ).strip(),

                "name": str(
                    row.get(columns["employee_name"], "")
                ).strip(),

                "department": str(
                    row.get("Department", "")
                ).strip(),

                "designation": str(
                    row.get("Designation", "")
                ).strip(),

                "email": str(
                    row.get("Email", "")
                ).strip(),

                "phone": str(
                    row.get("Phone", "")
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

                attendance_date = pd.to_datetime(
                    attendance_date,
                    errors="coerce",
                    dayfirst=True
                )

                if pd.notna(attendance_date):

                    employee["attendance_date"] = (
                        attendance_date.strftime("%d-%m-%Y")
                    )   

                    day = attendance_date.day

            print("=" * 60)
            print("Attendance Date")
            print("=" * 60)
            print(f"Employee ID     : {employee['employee_id']}")
            print(f"Employee Name   : {employee['name']}")
            print(f"Attendance Date : {employee['attendance_date']}")
            print(f"Calculated Day  : {day}")
            print("=" * 60)

            # =====================================================
            # Punch In / Punch Out
            # =====================================================

            in_time = self.convert_time(
                row.get(columns["in_time"])
            )

            out_time = self.convert_time(
                row.get(columns["out_time"])
            )

            employee["punch_in"] = self.format_time(
                in_time
            )

            employee["punch_out"] = self.format_time(
                out_time
            )
            # =====================================================
            # Daily Overtime Calculation
            # =====================================================

            imported_minutes = 0

            if columns["ot"] is not None:

                imported_ot = self.read_ot(
                    row.get(columns["ot"])
                ) 

                try:

                    hh, mm = imported_ot.split(":")

                    imported_minutes = (
                        int(hh) * 60
                        + int(mm)
                    )

                except Exception:

                    imported_minutes = 0

            calculated_minutes = (
                self.overtime.calculate_daily_overtime(
                    out_time
                )
            )

            final_minutes = max(
                imported_minutes,
                calculated_minutes
            )

            employee["daily_ot_minutes"] = final_minutes

            employee["daily_ot"] = (
                self.overtime.minutes_to_time(
                    final_minutes
                )
            )

            if final_minutes > 0:

                summary["overtime"] += 1

            print("=" * 60)
            print("Daily Overtime")
            print("=" * 60)
            print(f"Employee ID      : {employee['employee_id']}")
            print(f"Imported OT      : {imported_minutes} Minutes")
            print(f"Calculated OT    : {calculated_minutes} Minutes")
            print(f"Final OT         : {employee['daily_ot']}")
            print("=" * 60)

        # =====================================================
        # Save Monthly Overtime
        # =====================================================

            employee = self.overtime.process(
                employee=employee,
                punch_out=out_time,
                day=day
            )

            print("=" * 60)
            print("Monthly Overtime")
            print("=" * 60)
            print(f"Employee ID      : {employee['employee_id']}")
            print(f"Attendance Date  : {employee['attendance_date']}")
            print(f"Daily OT         : {employee['daily_ot']}")
            print(f"Monthly OT       : {employee['monthly_ot']}")
            print(f"Remaining OT     : {employee['remaining_ot']}")
            print(f"Monthly Status   : {employee['monthly_status']}")

            for d in range(1, 32):

                value = employee.get(f"Day{d}", "00:00")

                if value != "00:00":

                    print(f"Day{d:<2} : {value}")

            print("=" * 60)
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

                employee["status"].append(
                    "Absent"
                )

            elif attendance == "P/A":

                summary["half_day"] += 1

                employee["daily_status"] = "Half Day"

                employee["status"].append(
                    "Half Day"
                )

            else:

                employee["daily_status"] = "Unknown"

            # =====================================================
            # Late Punch
            # =====================================================

            if (
                CHECK_LATE_IN
                and self.overtime.is_late_punch(
                    in_time,
                    self.grace_time
                )
            ):

                summary["late_in"] += 1

                employee["status"].append(
                    "Late Punch"
                )

            # =====================================================
            # Early Out
            # =====================================================

            if (
                CHECK_EARLY_OUT
                and self.overtime.is_early_out(
                    out_time
                )
            ):

                summary["early_out"] += 1

                employee["status"].append(
                    "Early Out"
                )

        # =====================================================
        # Missing Punch In
        # =====================================================

            if (
                CHECK_MISSING_IN
                and in_time is None
            ):

                summary["missing_in"] += 1

                employee["status"].append(
                    "Missing Punch In"
                )

        # =====================================================
        # Missing Punch Out
        # =====================================================

            if (
                CHECK_MISSING_OUT
                and out_time is None
            ):

                summary["missing_out"] += 1

                employee["status"].append(
                    "Missing Punch Out"
                )

        # =====================================================
        # Monthly OT Status Summary
        # =====================================================

            if employee["monthly_status"] == WARNING_STATUS:

                summary["monthly_warning"] += 1

            elif employee["monthly_status"] == LIMIT_REACHED_STATUS:

                summary["monthly_limit_reached"] += 1

            elif employee["monthly_status"] == EXCEEDED_STATUS:

                summary["monthly_ot_exceeded"] += 1

        # =====================================================
        # Generate Notification
        # =====================================================

            employee["notification"] = (
                self.notification.generate_message(
                    employee
                )
            )

        # =====================================================
        # Store Employee
        # =====================================================

            employees.append(employee)

            print("=" * 60)
            print("Employee Processed Successfully")
            print("=" * 60)
            print(f"Employee ID     : {employee['employee_id']}")
            print(f"Employee Name   : {employee['name']}")
            print(f"Daily Status    : {employee['daily_status']}")
            print(f"Daily OT        : {employee['daily_ot']}")
            print(f"Monthly OT      : {employee['monthly_ot']}")
            print("=" * 60)
            
            # =====================================================
            # End Employee Loop
            # =====================================================

        try:

            del dataframe

        except NameError:

            pass

        gc.collect()

        # =====================================================
        # Processing Completed
        # =====================================================

        end_time = time.perf_counter()

        processing_time = round(
            end_time - start_time,
            2
        )

        summary["processing_time"] = processing_time

        summary["total_processed"] = len(
            employees
        )

        # =====================================================
        # Generate HR Report
        # =====================================================

        try:

            hr_report_path = (
                self.hr_report.generate(
                    employees=employees,
                    summary=summary
                )
            )

            summary["hr_report"] = (
                hr_report_path
            )

            print("=" * 60)
            print("HR Report Generated Successfully")
            print(hr_report_path)
            print("=" * 60)

        except Exception as error:

            print("=" * 60)
            print("HR Report Generation Failed")
            print(error)
            print("=" * 60)

            summary["hr_report"] = None

        # =====================================================
        # Generate Notification Summary
        # =====================================================

        try:

            summary["notification_summary"] = (
                self.notification.generate_summary(
                    employees,
                    summary
                )
            )

        except Exception as error:

            print(error)

            summary["notification_summary"] = ""

        # =====================================================
        # Processing Statistics
        # =====================================================

        print("\n" + "=" * 60)
        print("Attendance Processing Completed")
        print("=" * 60)

        print(
            f"Total Employees          : {summary['total']}"
        )

        print(
            f"Present                  : {summary['present']}"
        )

        print(
            f"Absent                   : {summary['absent']}"
        )   

        print(
            f"Half Day                 : {summary['half_day']}"
        )

        print(
            f"Late Punch               : {summary['late_in']}"
        )

        print(
            f"Early Out                : {summary['early_out']}"
        )

        print(
            f"Missing Punch In         : {summary['missing_in']}"
        )

        print(
            f"Missing Punch Out        : {summary['missing_out']}"
        )

        print(
            f"Employees With OT        : {summary['overtime']}"
        )

        print(
            f"Monthly Warning          : {summary['monthly_warning']}"
        )

        print(
            f"Monthly Limit Reached    : {summary['monthly_limit_reached']}"
        )

        print(
            f"Monthly OT Exceeded      : {summary['monthly_ot_exceeded']}"
        )

        print(
            f"Processing Time          : {processing_time} Seconds"
        )

        print("=" * 60)

        # =====================================================
        # Sort Employees
        # =====================================================

        try:

            employees = sorted(

                employees,

                key=lambda employee: (

                    employee.get(
                        "employee_id",
                        ""
                    ),

                    employee.get(
                        "attendance_date",
                        ""
                    )

                )

            )

        except Exception as error:

            print(
                f"Sorting Error : {error}"
            )

        # =====================================================
        # Final Memory Cleanup
        # =====================================================

        gc.collect()

        # =====================================================
        # Return Result
        # =====================================================

        return {

            "success": True,

            "employees": employees,

            "summary": summary,

            "processing_time": processing_time

        }