"""
=========================================================
Attendance Notification System Pro
Attendance Checker
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

import os
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
)

from services.database_manager import DatabaseManager
from services.overtime_checker import OvertimeManager
from services.hr_report import HRReportGenerator


class AttendanceChecker:
    """
    Enterprise Attendance Processing Engine
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

        self.database = DatabaseManager()

        self.ot_manager = OvertimeManager()

        self.hr_generator = HRReportGenerator()
        # =====================================================
    # Read Attendance File
    # =====================================================

    def read_file(self, filepath):

        extension = os.path.splitext(
            filepath
        )[1].lower()

        if extension == ".csv":

            try:

                dataframe = pd.read_csv(
                    filepath,
                    encoding="utf-8"
                )

            except Exception:

                dataframe = pd.read_csv(
                    filepath,
                    encoding="latin1"
                )

        elif extension in [".xlsx", ".xls"]:

            dataframe = pd.read_excel(
                filepath
            )

        else:

            raise ValueError(
                "Unsupported file format."
            )

        # ---------------------------------------
        # Remove extra spaces from column names
        # ---------------------------------------

        dataframe.columns = [

            str(column).strip()

            for column in dataframe.columns

        ]

        # ---------------------------------------
        # Remove completely empty rows
        # ---------------------------------------

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
    # Convert Time
    # =====================================================

    def convert_time(self, value):

        if pd.isna(value):
            return None

        if value is None:
            return None

        value = str(value).strip()

        if value in [
            "",
            "-",
            "--",
            "nan",
            "NaN",
            "None"
        ]:
            return None

        # ---------------------------------------
        # Supported Time Formats
        # ---------------------------------------

        formats = [

            "%H:%M",
            "%H:%M:%S",
            "%I:%M %p",
            "%I:%M:%S %p",
            "%I:%M%p"

        ]

        for fmt in formats:

            try:

                return datetime.strptime(
                    value,
                    fmt
                )

            except Exception:

                continue

        # ---------------------------------------
        # Normalize separators
        # ---------------------------------------

        value = value.replace(".", ":")
        value = value.replace("-", ":")

        try:

            return datetime.strptime(
                value,
                "%H:%M"
            )

        except Exception:

            return None
        # =====================================================
    # Format Time
    # =====================================================

    def format_time(self, value):

        if value is None:

            return "--"

        if not isinstance(value, datetime):

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

        # -----------------------------------------
        # Read Attendance File
        # -----------------------------------------

        dataframe = self.read_file(
            attendance_file
        )

        if dataframe.empty:

            raise ValueError(
                "Attendance file is empty."
            )

        # -----------------------------------------
        # Required Columns
        # -----------------------------------------

        required_columns = [

            "Employee No",

            "Employee Name",

            "Attendance Date",

            "IN Time",

            "OUT Time"

        ]

        missing_columns = [

            column

            for column in required_columns

            if column not in dataframe.columns

        ]

        if missing_columns:

            raise ValueError(

                "Missing required columns: "

                + ", ".join(missing_columns)

            )

        # -----------------------------------------
        # Initialize
        # -----------------------------------------

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

        # -----------------------------------------
        # Process Employees
        # -----------------------------------------

        for _, row in dataframe.iterrows():

            summary["total"] += 1

            employee = {}

            employee["employee_id"] = str(
                row.get("Employee No", "")
            ).strip()

            employee["name"] = str(
                row.get("Employee Name", "")
            ).strip()

            employee["unit"] = str(
                row.get("Unit", "")
            ).strip()

            employee["department"] = str(
                row.get("Department", "")
            ).strip()

            employee["designation"] = str(
                row.get("Designation", "")
            ).strip()

            employee["attendance_date"] = str(
                row.get("Attendance Date", "")
            ).strip()

            employee["approval_status"] = str(
                row.get("Approval Status", "")
            ).strip()

            employee["remarks"] = str(
                row.get("Remarks", "")
            ).strip()

            employee["email"] = str(
                row.get("Email", "")
            ).strip()

            employee["status"] = []

            employee["notification"] = ""
            # =====================================================
            # Punch Details
            # =====================================================

            in_time = self.convert_time(
                row.get("IN Time", "")
            )

            out_time = self.convert_time(
                row.get("OUT Time", "")
            )

            employee["punch_in"] = self.format_time(
                in_time
            )

            employee["punch_out"] = self.format_time(
                out_time
            )

            late = str(
                row.get("Late IN(HH:MM)", "")
            ).strip()

            early = str(
                row.get("Early OUT(HH:MM)", "")
            ).strip()

            employee["daily_ot"] = str(
                row.get("OT HRS", "00:00")
            ).strip()

            # =====================================================
            # Missing Punch In
            # =====================================================

            if CHECK_MISSING_IN and in_time is None:

                employee["status"].append(
                    "Missing Punch In"
                )

                summary["missing_in"] += 1

            # =====================================================
            # Missing Punch Out
            # =====================================================

            if CHECK_MISSING_OUT and out_time is None:

                employee["status"].append(
                    "Missing Punch Out"
                )

                summary["missing_out"] += 1

            # =====================================================
            # Late Punch
            # =====================================================

            if (
                CHECK_LATE_IN
                and late not in [
                    "",
                    "-",
                    "--",
                    "00:00",
                    "00:00:00",
                    "0",
                    "0.0",
                    "nan",
                    "NaN"
                ]
            ):

                employee["status"].append(
                    f"Late Punch ({late})"
                )

                summary["late_in"] += 1

            # =====================================================
            # Early Out
            # =====================================================

            if (
                CHECK_EARLY_OUT
                and early not in [
                    "",
                    "-",
                    "--",
                    "00:00",
                    "00:00:00",
                    "0",
                    "0.0",
                    "nan",
                    "NaN"
                ]
            ):

                employee["status"].append(
                    f"Early Out ({early})"
                )

                summary["early_out"] += 1

            # =====================================================
            # Daily & Monthly Overtime
            # =====================================================

            employee = self.ot_manager.process(
                employee,
                out_time
            )

            if employee["daily_ot_minutes"] > 0:

                employee["status"].append(
                    f"Daily OT ({employee['daily_ot']})"
                )

                summary["overtime"] += 1

            if employee["monthly_status"] == "Warning":

                employee["status"].append(
                    "Monthly OT Warning"
                )

                summary["warning"] += 1

            elif employee["monthly_status"] == "Limit Reached":

                employee["status"].append(
                    "Monthly OT Limit Reached"
                )

                summary["limit_reached"] += 1

            elif employee["monthly_status"] == "Exceeded":

                employee["status"].append(
                    "Monthly OT Exceeded"
                )

                summary["monthly_ot_exceeded"] += 1

            # =====================================================
            # Present Employee
            # =====================================================

            if len(employee["status"]) == 0:

                employee["status"].append(
                    "On Time"
                )

                summary["present"] += 1
                # =====================================================
            # Employee Notification
            # =====================================================

            notification = []

            notification.append(
                f"👤 Employee : {employee['name']}"
            )

            notification.append(
                f"🆔 Employee ID : {employee['employee_id']}"
            )

            notification.append(
                f"🏢 Department : {employee['department']}"
            )

            notification.append(
                f"💼 Designation : {employee['designation']}"
            )

            notification.append("")

            notification.append(
                f"📅 Attendance Date : {employee['attendance_date']}"
            )

            notification.append(
                f"🕘 Punch In : {employee['punch_in']}"
            )

            notification.append(
                f"🕔 Punch Out : {employee['punch_out']}"
            )

            notification.append("")

            # ==========================================
            # Attendance Alerts
            # ==========================================

            if "Missing Punch In" in employee["status"]:

                notification.append(
                    "❌ Missing Punch In."
                )

            if "Missing Punch Out" in employee["status"]:

                notification.append(
                    "❌ Missing Punch Out."
                )

            if any(
                "Late Punch" in status
                for status in employee["status"]
            ):

                notification.append(
                    "⚠️ Late Punch Detected."
                )

            if any(
                "Early Out" in status
                for status in employee["status"]
            ):

                notification.append(
                    "⚠️ Early Punch Out."
                )

            notification.append("")

            # ==========================================
            # Overtime Details
            # ==========================================

            notification.append(
                f"🕒 Daily OT : {employee['daily_ot']}"
            )

            notification.append(
                f"📅 Monthly OT : {employee['monthly_ot']}"
            )

            notification.append(
                f"⏳ Remaining Monthly OT : {employee['remaining_ot']}"
            )

            notification.append("")

            # ==========================================
            # Monthly OT Status
            # ==========================================

            if employee["monthly_status"] == "Warning":

                notification.append(
                    "⚠️ Your monthly overtime has crossed the warning limit."
                )

            elif employee["monthly_status"] == "Limit Reached":

                notification.append(
                    "🚨 Monthly OT Limit Reached (25 Hours)."
                )

                notification.append(
                    "Further overtime requires HR approval."
                )

            elif employee["monthly_status"] == "Exceeded":

                notification.append(
                    "❌ Monthly OT Limit Exceeded."
                )

                notification.append(
                    "Please contact the HR Department."
                )

            else:

                notification.append(
                    "✅ Monthly OT is within the permitted limit."
                )

            notification.append("")
            notification.append("Regards,")
            notification.append("HR Department")

            employee["notification"] = "\n".join(
                notification
            )

            employees.append(
                employee
            )

        # =====================================================
        # Generate HR Report
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
        # Return Result
        # =====================================================

        return {

            "summary": {

                "total": summary["total"],

                "present": summary["present"],

                "late_in": summary["late_in"],

                "early_out": summary["early_out"],

                "missing_in": summary["missing_in"],

                "missing_out": summary["missing_out"],

                "overtime": summary["overtime"],

                "warning": summary["warning"],

                "limit_reached": summary["limit_reached"],

                "monthly_ot_exceeded": summary["monthly_ot_exceeded"]

            },

            "employees": employees,

            "hr_report": hr_report,

            "late_punch_report": late_punch_report

        }