"""
=========================================================
Attendance Notification System Pro
Enterprise Report Generator
Version : 16.0 Enterprise
Developed by Maharajan
=========================================================
"""

import os
from datetime import datetime

import pandas as pd

from config import (
    REPORT_FOLDER,
    COMPANY_NAME,
    MONTHLY_OT_DATABASE
)


class ReportGenerator:
    """
    Enterprise Report Generator
    Version 16.0
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.report_folder = REPORT_FOLDER

        os.makedirs(
            self.report_folder,
            exist_ok=True
        )

    # =====================================================
    # Current Timestamp
    # =====================================================

    def current_time(self):

        return datetime.now().strftime(
            "%d-%b-%Y %H:%M:%S"
        )

    # =====================================================
    # Current Date
    # =====================================================

    def current_date(self):

        return datetime.now().strftime(
            "%d-%b-%Y"
        )

    # =====================================================
    # Safe Value
    # =====================================================

    def safe(self, value, default=""):

        if value is None:
            return default

        if str(value).strip() == "":
            return default

        return value
    # =====================================================
    #    Attendance Report
    # =====================================================

    def generate_excel(
        self,
        employees,
        filename="Attendance_Report.xlsx"
    ):

        report_path = os.path.join(
            self.report_folder,
            filename
        )

        records = []

        for number, employee in enumerate(
            employees,
            start=1
        ):

            row = {

                "S.No": number,

                "Employee ID": employee.get(
                    "employee_id",
                    ""
                ),

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

                "Attendance Date": employee.get(
                    "attendance_date",
                    self.current_date()
                ),

                "Punch In": employee.get(
                    "punch_in",
                    "--"
                ),

                "Punch Out": employee.get(
                    "punch_out",
                    "--"
                ),

                "Daily OT": employee.get(
                    "daily_ot",
                    "00:00"
                ),

                "Daily Status": employee.get(
                    "daily_status",
                    "Normal"
                ),

                "Monthly OT": employee.get(
                    "monthly_ot",
                    "00:00"
                ),

                "Monthly OT Minutes": employee.get(
                "monthly_ot_minutes",
                    0
                ),

                "Remaining OT": employee.get(
                    "remaining_ot",
                    "25:00"
                ),

                "Remaining OT Minutes": employee.get(
                    "remaining_ot_minutes",
                    1500
                ),

                "Monthly Status": employee.get(
                    "monthly_status",
                    "Normal"
                ),

                "Notification": employee.get(
                    "notification",
                    ""
                ),

                "Notification Status": employee.get(
                    "notification_status",
                    "Pending"
                )

            }

            records.append(row)

        dataframe = pd.DataFrame(records)

        with pd.ExcelWriter(

            report_path,

            engine="openpyxl",

            mode="w"

        ) as writer:

            dataframe.to_excel(

                writer,

                index=False,

                sheet_name="Attendance"

            )

            worksheet = writer.sheets["Attendance"]

            for column_cells in worksheet.columns:

                length = max(

                    len(str(cell.value))
                    if cell.value is not None
                    else 0

                    for cell in column_cells

                )

                worksheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = max(
                    15,
                    length + 3
                )

        return report_path  
    # =====================================================
    # Generate Summary
    # =====================================================

    def generate_summary(
        self,
        summary
    ):

        return {

            "Company": COMPANY_NAME,

            "Generated On": self.current_time(),

            "Total Employees": summary.get(
                "total",
                0
            ),

            "Present": summary.get(
                "present",
                0
            ),

            "Absent": summary.get(
                "absent",
                0
            ),

            "Half Day": summary.get(
                "half_day",
                0
            ),

            "Late Punch": summary.get(
                "late_in",
                0
            ),

            "Early Out": summary.get(
                "early_out",
                0
            ),

            "Missing Punch In": summary.get(
                "missing_in",
                0
            ),

            "Missing Punch Out": summary.get(
                "missing_out",
                0
            ),

            "Overtime Employees": summary.get(
                "overtime",
                0
            ),

            "Monthly OT Warning": summary.get(
                "monthly_warning",
                0
            ),

            "Monthly OT Limit Reached": summary.get(
                "monthly_limit_reached",
                0
            ),

            "Monthly OT Exceeded": summary.get(
                "monthly_ot_exceeded",
                0
            )

        }


    # =====================================================
    # Dashboard Report
    # =====================================================

    def generate_dashboard_report(
        self,
        summary
    ):

        dashboard = [

            {
                "Title": "Total Employees",
                "Count": summary.get(
                    "total",
                    0
                )
            },

            {
                "Title": "Present",
                "Count": summary.get(
                    "present",
                    0
                )
            },

            {
                "Title": "Absent",
                "Count": summary.get(
                    "absent",
                    0
                )
            },

            {
                "Title": "Half Day",
                "Count": summary.get(
                    "half_day",
                    0
                )
            },

            {
                "Title": "Late Punch",
                "Count": summary.get(
                    "late_in",
                    0
                )
            },

            {
                "Title": "Early Out",
                "Count": summary.get(
                    "early_out",
                    0
                )
            },

            {
                "Title": "Missing Punch In",
                "Count": summary.get(
                    "missing_in",
                    0
                )
            },

            {
                "Title": "Missing Punch Out",
                "Count": summary.get(
                    "missing_out",
                    0
                )   
            },

            {
                "Title": "OT Employees",
                "Count": summary.get(
                    "overtime",
                    0
                )
            },

            {
                "Title": "Monthly Warning",
                "Count": summary.get(
                    "monthly_warning",
                    0
                )
            },

            {
                "Title": "Limit Reached",
                "Count": summary.get(
                    "monthly_limit_reached",
                    0
                )
            },

            {
                "Title": "Exceeded",
                "Count": summary.get(
                    "monthly_ot_exceeded",
                    0
                )
            }

        ]

        return dashboard
    # =====================================================
    # Monthly OT Report
    # =====================================================

    def generate_monthly_ot_report(
        self,
        employees,
        filename="Monthly_OT_Report.xlsx"
    ):

        report_path = os.path.join(
            self.report_folder,
            filename
        )

        records = []

        for number, employee in enumerate(
            employees,
            start=1
        ):

            row = {

                "S.No": number,

                "Employee ID": employee.get(
                    "employee_id",
                    ""
                ),

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
                )

            }

            # -----------------------------------------
            # Day1 - Day31
            # -----------------------------------------

            for day in range(1, 32):

                row[f"Day{day}"] = employee.get(
                    f"Day{day}",
                    "00:00"
                )

            # -----------------------------------------
            # Monthly Information
            # -----------------------------------------

            row["Daily OT"] = employee.get(
                "daily_ot",
                "00:00"
            )

            row["Daily Status"] = employee.get(
                "daily_status",
                "Normal"
            )

            row["Monthly OT"] = employee.get(
                "monthly_ot",
                "00:00"
            )

            row["Monthly OT Minutes"] = employee.get(
                "monthly_ot_minutes",
                0
            )

            row["Remaining OT"] = employee.get(
                "remaining_ot",
                "25:00"
            )

            row["Remaining OT Minutes"] = employee.get(
                "remaining_ot_minutes",
                1500
            )

            row["Monthly Status"] = employee.get(
                "monthly_status",
                "Normal"
            )

            row["Notification Status"] = employee.get(
                "notification_status",
                "Pending"
            )

            row["Last Updated"] = employee.get(
                "last_updated",
                self.current_time()
            )

            records.append(row)

        dataframe = pd.DataFrame(records)

        with pd.ExcelWriter(
            report_path,
            engine="openpyxl",
            mode="w"
        ) as writer:

            dataframe.to_excel(
                writer,
                index=False,
                sheet_name="Monthly OT"
            )

            worksheet = writer.sheets["Monthly OT"]

            for column_cells in worksheet.columns:

                length = max(

                    len(str(cell.value))
                    if cell.value is not None
                    else 0

                    for cell in column_cells

                )

                worksheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = max(
                    15,
                    length + 3
                )

        return report_path
    # =====================================================
    # Load Monthly OT Database
    # =====================================================

    def load_monthly_database(self):

        if not os.path.exists(MONTHLY_OT_DATABASE):

            return pd.DataFrame()

        try:

            dataframe = pd.read_excel(

                MONTHLY_OT_DATABASE,

                engine="openpyxl"

            )

            dataframe.fillna(

                "",

                inplace=True

            )

            return dataframe

        except Exception as error:

            print(

                f"Monthly Database Load Error : {error}"

            )

            return pd.DataFrame()


    # =====================================================
    #    Export Monthly OT Database
    # =====================================================

    def export_monthly_database(

        self,

        filename="Monthly_OT_Database.xlsx",

        employees=None

    ):

        if employees is None:

            dataframe = self.load_monthly_database()

        else:

            records = []

            for employee in employees:

                row = {

                    "Employee ID": employee.get(
                        "employee_id",
                        ""
                    ),

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
            # Day1 - Day31
            # ------------------------------------------

                for day in range(1, 32):

                    row[f"Day{day}"] = employee.get(

                        f"Day{day}",

                        "00:00"

                    )

            # ------------------------------------------
            # Daily / Monthly OT Details
            # ------------------------------------------

                row["Daily OT"] = employee.get(
                    "daily_ot",
                    "00:00"
                )

                row["Daily Status"] = employee.get(
                    "daily_status",
                    "Normal"
                )

                row["Monthly OT"] = employee.get(
                    "monthly_ot",
                    "00:00"
                )

                row["Monthly OT Minutes"] = employee.get(
                    "monthly_ot_minutes",
                    0
                )

                row["Remaining OT"] = employee.get(
                    "remaining_ot",
                    "25:00"
                )

                row["Remaining OT Minutes"] = employee.get(
                    "remaining_ot_minutes",
                    1500
                )

                row["Monthly Status"] = employee.get(
                    "monthly_status",
                    "Normal"
                )

                row["Notification"] = employee.get(
                    "notification",
                    ""
                )

                row["Notification Status"] = employee.get(
                    "notification_status",
                    "Pending"
                )

                row["Last Updated"] = employee.get(
                    "last_updated",
                    self.current_time()
                )

                records.append(row)

            dataframe = pd.DataFrame(records)

        report_path = os.path.join(

            self.report_folder,

            filename

        )

        if dataframe.empty:

            dataframe = pd.DataFrame(columns=[

                "Employee ID",
                "Employee Name",
                "Department",
                "Designation",
                "Email",
                "Phone",

                *[f"Day{i}" for i in range(1, 32)],

                "Daily OT",
                "Daily Status",

                "Monthly OT",
                "Monthly OT Minutes",

                "Remaining OT",
                "Remaining OT Minutes",

                "Monthly Status",

                "Notification",

                "Notification Status",

                "Last Updated"

            ])

        with pd.ExcelWriter(

            report_path,

            engine="openpyxl",

            mode="w"

        ) as writer:

            dataframe.to_excel(

                writer,

                index=False,

                sheet_name="Monthly Database"

            )

            worksheet = writer.sheets["Monthly Database"]

            for column_cells in worksheet.columns:

                length = max(

                    len(str(cell.value))
                    if cell.value is not None
                    else 0

                    for cell in column_cells

                )

                worksheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = max(
                    15,
                    length + 3
                )   

        return report_path
    # =====================================================
    # Complete Enterprise Report
    # =====================================================

    def generate_complete_report(
        self,
        employees,
        summary
    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    # ==========================================
    # Attendance Report
    # ==========================================

        attendance_report = self.generate_excel(

            employees,

            f"Attendance_Report_{timestamp}.xlsx"

        )

    # ==========================================
    # Monthly OT Report
    # ==========================================

        monthly_ot_report = self.generate_monthly_ot_report(

            employees,

            f"Monthly_OT_Report_{timestamp}.xlsx"

        )

    # ==========================================
    # Monthly Database
    # ==========================================

        database_report = self.export_monthly_database(

            f"Monthly_OT_Database_{timestamp}.xlsx",

            employees

        )

    # ==========================================
    # Summary
    # ==========================================

        summary_report = self.generate_summary(
            summary
        )

    # ==========================================
    # Dashboard Summary
    # ==========================================

        dashboard_report = self.generate_dashboard_report(
            summary
        )   

    # ==========================================
    # Top 10 Monthly OT Employees
    # ==========================================

        top_ot_employees = sorted(

            employees,

            key=lambda employee: employee.get(
                "monthly_ot_minutes",
                0
            ),

            reverse=True

        )[:10]

    # ==========================================
    # Warning Employees
    # ==========================================

        warning_employees = [

            employee

            for employee in employees

            if employee.get(
                "monthly_status",
                ""
            ) == "Warning"

        ]

    # ==========================================
    # Limit Reached Employees
    # ==========================================

        limit_reached_employees = [

            employee

            for employee in employees

            if employee.get(
                "monthly_status",
                ""
            ) == "Limit Reached"

        ]

    # ==========================================
    # Exceeded Employees
    # ==========================================

        exceeded_employees = [

            employee

            for employee in employees

            if employee.get(
                "monthly_status",
                ""
            ) == "Exceeded"

        ]

    # ==========================================
    # Dashboard Counts
    # ==========================================

        dashboard_counts = {

            "total": len(employees),

            "warning": len(warning_employees),

            "limit_reached": len(limit_reached_employees),

            "exceeded": len(exceeded_employees)

        }

    # ==========================================
    # Return Complete Report
    # ==========================================

        return {

            "attendance_report": attendance_report,

            "monthly_ot_report": monthly_ot_report,

            "database_report": database_report,

            "summary_report": summary_report,

            "dashboard_report": dashboard_report,

            "dashboard_counts": dashboard_counts,

            "top_ot_employees": top_ot_employees,

            "warning_employees": warning_employees,

            "limit_reached_employees": limit_reached_employees,

            "exceeded_employees": exceeded_employees,

            "generated_on": self.current_time(),

            "company": COMPANY_NAME,

            "employee_count": len(employees),

            "employees": employees,

            "summary": summary

        }