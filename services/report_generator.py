"""
=========================================================
Attendance Notification System
Report Generator
Version : 1.0
=========================================================
"""

import os
import pandas as pd
from datetime import datetime

from config import REPORT_FOLDER


class ReportGenerator:

    def __init__(self):

        self.report_folder = REPORT_FOLDER

    # =====================================================
    # Generate Excel Report
    # =====================================================

    def generate_report(self, result, original_filename):

        summary = result["summary"]

        employees = result["employees"]

        report_rows = []

        for employee in employees:

            report_rows.append({

                "Employee ID": employee.get("employee_id", ""),

                "Employee Name": employee.get("name", ""),

                "Phone": employee.get("phone", ""),

                "Punch In": employee.get("punch_in", ""),

                "Punch Out": employee.get("punch_out", ""),

                "Status": ", ".join(employee.get("status", [])),

                "Notification": employee.get("notification", ""),

                "Late Minutes": employee.get("late_minutes", 0),

                "Early Minutes": employee.get("early_minutes", 0),

                "Overtime Minutes": employee.get("overtime_minutes", 0)

            })

        employee_df = pd.DataFrame(report_rows)

        summary_df = pd.DataFrame([{

            "Total Employees": summary["total"],

            "Late Punch In": summary["late_in"],

            "Missing Punch In": summary["missing_in"],

            "Missing Punch Out": summary["missing_out"],

            "Early Punch Out": summary["early_out"],

            "Overtime": summary["overtime"]

        }])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_name = f"Attendance_Report_{timestamp}.xlsx"

        report_path = os.path.join(

            self.report_folder,

            report_name

        )

        with pd.ExcelWriter(

            report_path,

            engine="openpyxl"

        ) as writer:

            summary_df.to_excel(

                writer,

                sheet_name="Summary",

                index=False

            )

            employee_df.to_excel(

                writer,

                sheet_name="Employees",

                index=False

            )

        return report_path
    