"""
=========================================================
Attendance Notification System Pro
Enterprise Attendance Checker
Version : 17.0 Enterprise
Developed by Maharajan
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
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)

from services.database_manager import DatabaseManager
from services.overtime_manager import OvertimeManager
from services.notification_service import NotificationService
from services.hr_report import HRReportGenerator


class AttendanceChecker:
    """
    Enterprise Attendance Processing Engine
    Version 17.0 Enterprise
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

    # =====================================================
    # Read CSV
    # =====================================================

        if extension == ".csv":

            dataframe = None

            for encoding in [
                "utf-8",
                "utf-8-sig",
                "cp1252",
                "latin1"
            ]:

                try:

                    dataframe = pd.read_csv(
                        filepath,
                        encoding=encoding,
                        low_memory=False
                    )

                    break

                except Exception:
                    pass

            if dataframe is None:

                raise Exception(
                    "Unable to read CSV file."
                )

    # =====================================================
    # Read Excel
    # =====================================================

        elif extension in [".xlsx", ".xls"]:

            dataframe = pd.read_excel(
                filepath,
                engine="openpyxl"
            )

    # =====================================================
    # Unsupported File
    # =====================================================

        else:

            raise Exception(
                f"Unsupported file : {extension}"
            )

    # =====================================================
    # Clean Column Names
    # =====================================================

        dataframe.columns = [

            str(column)
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()

            for column in dataframe.columns

        ]

    # =====================================================
    # Remove Empty Rows
    # =====================================================

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

        available = {

            str(column).strip().lower(): column

            for column in dataframe.columns

        }

        for alias in aliases:

            alias = alias.strip().lower()

            if alias in available:

                return available[alias]

        return None


    # =====================================================
    # Detect Columns
    # =====================================================

    def detect_columns(
        self,
        dataframe
    ):

        columns = {
            
            "department": self.find_column(
                dataframe,
                ["Department"]
            ),
            
            "designation": self.find_column(
                dataframe,
                ["Designation"]
            ),
            
            "email": self.find_column(
                dataframe,
                ["Email"]
            ),
            
            "phone": self.find_column(
                dataframe,
                ["Phone"]
            ),

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

        return columns


    # =====================================================
    # Convert Time
    # =====================================================

    def convert_time(self, value):

        if value is None or pd.isna(value):

            return None

        if isinstance(value, datetime):

            return value

        if isinstance(value, pd.Timestamp):

            return value.to_pydatetime()

        if isinstance(value, (int, float)):

            try:

                value = float(value)

                if value >= 1:

                    value = value % 1

                seconds = round(value * 86400)

                hour = (seconds // 3600) % 24
                minute = (seconds % 3600) // 60

                return datetime.strptime(
                    f"{hour:02d}:{minute:02d}",
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
                pass

        return None


    # =====================================================
    # Format Time
    # =====================================================

    def format_time(self, value):

        if value is None:

            return "--"

        return value.strftime("%H:%M")


    # =====================================================
    # Read OT
    # =====================================================

    def read_ot(self, value):

        if value is None or pd.isna(value):

            return "00:00"

        value = str(value).strip()

        if value in self.empty_values:

            return "00:00"
        try:

            value = value.replace(".", ":")

            if ":" in value:

                hh, mm = value.split(":")

                return f"{int(hh):02d}:{int(mm):02d}"

            return f"{int(float(value)):02d}:00"

        except Exception:

            return "00:00"
        # =====================================================
        #  Process Attendance File
        # =====================================================

    def process_excel(self, attendance_file):

        start_time = time.perf_counter()

        dataframe = self.read_file(
            attendance_file
        )

        if dataframe.empty:

            raise Exception(
                "Attendance file is empty."
            )

        columns = self.detect_columns(
            dataframe
        )

        employees = []

        summary: dict[str, Any]= {

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
        # ==========================================
        # Process Each Employee
        # ==========================================

        for _, row in dataframe.iterrows():
            
            attendance_date = row.get(
                columns["attendance_date"],
                ""
            )


            print("=" * 70)
            print("Employee ID      :", row.get(columns["employee_id"], ""))
            print("Attendance Date(Excel):", attendance_date)
            print("=" * 70)

            summary["total"] += 1

            employee = {
                
                "attendance_date": str(attendance_date).strip(),

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
                        columns["department"],
                        ""
                    )
                ).strip(),

                    "designation": str(
                    row.get(
                        columns["designation"],
                        ""
                    )
                ).strip(),

                "email": str(
                    row.get(
                        columns["email"],
                        ""
                    )
                ).strip(),

                "phone": str(
                    row.get(
                        columns["phone"],
                        ""
                    )
                ).strip(),


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

                "notification": "",
                
                "current_day": 0,

            }

            # ==========================================
            # Attendance Date
            # ==========================================

            attendance_date = pd.to_datetime(
                str(row.get(columns["attendance_date"], "")),
                errors="coerce",
                dayfirst=True
            )
            
            print("=" * 60)
            print("Raw Excel Date :", row.get(columns["attendance_date"]))
            print("Parsed Date    :", attendance_date)
            print("Current Day    :", attendance_date.day if not pd.isna(attendance_date) else "Invalid")
            print("=" * 60)
            
            if pd.isna(attendance_date):

                attendance_date = datetime.now()

            employee["attendance_date"] = attendance_date
            employee["current_day"] = int(attendance_date.day)

            current_day = employee["current_day"]
            
            if str(employee["employee_id"]) == "U1- 0005":
                print("=" * 60)
                print("Attendance Date:" ,attendance_date)
                print("Current Day:", current_day)
                print("=" * 60)

            # ==========================================
            # Punch Time
            # ==========================================

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

        # ==========================================
        # Daily OT
        # ==========================================

            imported_minutes = 0

            if columns["ot"] is not None:

                imported_ot = self.read_ot(

                    row.get(
                        columns["ot"]
                    )

                )

                try:

                    hh, mm = imported_ot.split(":")

                    imported_minutes = (
                        int(hh) * 60
                        + int(mm)
                    )

                except Exception:

                    imported_minutes = 0

            calculated_minutes = self.overtime.calculate_daily_overtime(
                out_time
            )

            final_minutes = max(

                imported_minutes,

                calculated_minutes

            )

            employee["daily_ot_minutes"] = final_minutes

            employee["daily_ot"] = self.overtime.minutes_to_time(
                final_minutes
            )
        # ==========================================
        # Save Monthly OT Database
        # ==========================================

            employee = self.overtime.process(

                employee=employee,

                punch_out=out_time,

                attendance_date=attendance_date

            )

            if employee["daily_ot_minutes"] > 0:

                summary["overtime"] += 1

        # ==========================================
        # Attendance Status
        # ==========================================

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

            # ==========================================
            # Late Punch
            # ==========================================

            if (

                CHECK_LATE_IN

                and

                self.overtime.is_late_punch(

                    in_time,

                    self.grace_time

                )

            ):

                summary["late_in"] += 1

                employee["status"].append(
                    "Late Punch"
                )

            # ==========================================
            # Early Out
            # ==========================================

            if (

                CHECK_EARLY_OUT

                and

                self.overtime.is_early_out(

                    out_time

                )

            ):

                summary["early_out"] += 1

                employee["status"].append(
                    "Early Out"
                )

            # ==========================================
            # Missing Punch In
            # ==========================================

            if (

                CHECK_MISSING_IN

                and

                in_time is None

            ):

                summary["missing_in"] += 1

                employee["status"].append(
                    "Missing Punch In"
                )

            # ==========================================
            # Missing Punch Out
            # ==========================================

            if (

                CHECK_MISSING_OUT

                and

                out_time is None

            ):

                summary["missing_out"] += 1

                employee["status"].append(
                    "Missing Punch Out"
                )
                # ==========================================
                # Monthly OT Status Summary
                # ==========================================

            if employee["monthly_status"] == WARNING_STATUS:

                summary["monthly_warning"] += 1

            elif employee["monthly_status"] == LIMIT_REACHED_STATUS:

                summary["monthly_limit_reached"] += 1

            elif employee["monthly_status"] == EXCEEDED_STATUS:

                summary["monthly_ot_exceeded"] += 1

            # ==========================================
            # Generate Employee Notification
            # ==========================================

            employee["notification"] = (

                self.notification.generate_message(

                    employee

                )

            )

            employee["notification_status"] = "Pending"

            # ==========================================
            # Store Employee
            # ==========================================

            employees.append(employee)

            print("=" * 60)
            print("Employee Processed Successfully")
            print("=" * 60)
            print(f"Employee ID      : {employee['employee_id']}")
            print(f"Employee Name    : {employee['name']}")
            print(f"Attendance Date  : {employee['attendance_date'].strftime('%d-%m-%Y')}")
            print(f"Punch In         : {employee['punch_in']}")
            print(f"Daily OT         : {employee['daily_ot']}")
            print(f"Monthly OT       : {employee['monthly_ot']}")
            print(f"Remaining OT     : {employee['remaining_ot']}")
            print(f"Monthly Status   : {employee['monthly_status']})")
            print("=" * 60)

        # ==========================================
        # Memory Cleanup
        # ==========================================

        try:

            del dataframe

        except Exception:

            pass

        gc.collect()

        # ==========================================
        # Processing Time
        # ==========================================

        processing_time = round(

            time.perf_counter() - start_time,

            2

        )

        summary["processing_time"] = processing_time

        summary["total_processed"] = len(employees)
        # =====================================================
        # Generate HR Report
        # =====================================================

        try:

            hr_report = self.hr_report.generate(

                employees=employees,

                summary=summary

            )

            summary["hr_report"] = hr_report

        except Exception as error:

            print(f"HR Report Error : {error}")

            summary["hr_report"] = ""

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

        except Exception:

            summary["notification_summary"] = ""
            
            summary["whatsapp_hr_report"] = summary.get("notification_summary", "")

        # =====================================================
        # Dashboard Summary
        # =====================================================

        dashboard = self.database.get_dashboard_summary()

        # =====================================================
        # Sort Employees
        # =====================================================

        employees = sorted(

            employees,

            key=lambda employee: (

                employee.get("employee_id", ""),

                employee.get("attendance_date", "")

            )

        )

        gc.collect()

        processing_time = round(

            time.perf_counter() - start_time,

            2

        )

        print("\n" + "=" * 70)
        print("ATTENDANCE PROCESSING COMPLETED")
        print("=" * 70)
        print(f"Employees          : {summary['total']}")
        print(f"Present            : {summary['present']}")
        print(f"Absent             : {summary['absent']}")
        print(f"Half Day           : {summary['half_day']}")
        print(f"Late Punch         : {summary['late_in']}")
        print(f"Early Out          : {summary['early_out']}")
        print(f"Missing Punch In   : {summary['missing_in']}")
        print(f"Missing Punch Out  : {summary['missing_out']}")
        print(f"OT Employees       : {summary['overtime']}")
        print(f"Monthly Warning    : {summary['monthly_warning']}")
        print(f"Limit Reached      : {summary['monthly_limit_reached']}")
        print(f"Exceeded           : {summary['monthly_ot_exceeded']}")
        print(f"Processing Time    : {processing_time} Seconds")
        print("=" * 70)

        # =====================================================
        # Return Result
        # =====================================================

        return {

            "success": True,

            "employees": employees,

            "summary": summary,

            "dashboard": dashboard,

            "processing_time": processing_time,

            "late_punch_report": summary.get(
                "late_punch_report",
                ""
            ),

            "notification_summary": summary.get(
                "notification_summary",
                ""
            ),

            "whatsapp_hr_report": summary.get(
                "notification_summary",
                ""
            )

        }