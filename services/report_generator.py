"""
=========================================================
Attendance Notification System Pro
Excel Report Generator
Version : 2.0
Developed by Maharajan
=========================================================
"""

import os

import pandas as pd

from datetime import datetime

from openpyxl.styles import (

    Font,

    PatternFill,

    Alignment,

    Border,

    Side

)

from openpyxl.utils import get_column_letter

from config import (

    REPORT_FOLDER,

    COMPANY_NAME

)


class ReportGenerator:

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.report_folder = REPORT_FOLDER

        # Header Style

        self.header_fill = PatternFill(

            start_color="0D6EFD",

            end_color="0D6EFD",

            fill_type="solid"

        )

        self.header_font = Font(

            bold=True,

            color="FFFFFF"

        )

        self.center = Alignment(

            horizontal="center",

            vertical="center"

        )

        thin = Side(style="thin")

        self.border = Border(

            left=thin,

            right=thin,

            top=thin,

            bottom=thin

        )

        self.title_font = Font(

            bold=True,

            size=16

        )

        self.summary_fill = PatternFill(

            start_color="D9EAD3",

            end_color="D9EAD3",

            fill_type="solid"

        )
        # =====================================================
    # Generate Excel Report
    # =====================================================

    def generate_report(

        self,

        result,

        original_filename

    ):

        summary = result["summary"]

        employees = result["employees"]

        # ==========================================
        # Employee Report Data
        # ==========================================

        report_rows = []

        for employee in employees:

            report_rows.append({

                "Employee ID": employee.get(
                    "employee_id", ""
                ),

                "Employee Name": employee.get(
                    "name", ""
                ),

                "Phone": employee.get(
                    "phone", ""
                ),

                "Email": employee.get(
                    "email", ""
                ),

                "Punch In": employee.get(
                    "punch_in", ""
                ),

                "Punch Out": employee.get(
                    "punch_out", ""
                ),

                "Status": ", ".join(
                    employee.get("status", [])
                ),

                "Remark": employee.get(
                    "remark", ""
                ),

                "Late Minutes": employee.get(
                    "late_minutes", 0
                ),

                "Early Minutes": employee.get(
                    "early_minutes", 0
                ),

                "Overtime Minutes": employee.get(
                    "overtime_minutes", 0
                ),

                "Notification": employee.get(
                    "notification", ""
                )

            })

        employee_df = pd.DataFrame(report_rows)

        # ==========================================
        # Summary Sheet
        # ==========================================

        present = (
            summary["total"]
            - summary["missing_in"]
        )

        summary_df = pd.DataFrame([{

            "Company": COMPANY_NAME,

            "Total Employees": summary["total"],

            "Present": present,

            "Late Punch": summary["late_in"],

            "Early Punch Out": summary["early_out"],

            "Missing Punch In": summary["missing_in"],

            "Missing Punch Out": summary["missing_out"],

            "Overtime": summary["overtime"]

        }])

        # ==========================================
        # Individual Report Sheets
        # ==========================================

        late_df = employee_df[
            employee_df["Status"].str.contains(
                "Late",
                case=False,
                na=False
            )
        ]

        missing_in_df = employee_df[
            employee_df["Status"].str.contains(
                "Missing Punch In",
                case=False,
                na=False
            )
        ]

        missing_out_df = employee_df[
            employee_df["Status"].str.contains(
                "Missing Punch Out",
                case=False,
                na=False
            )
        ]

        early_df = employee_df[
            employee_df["Status"].str.contains(
                "Early",
                case=False,
                na=False
            )
        ]

        overtime_df = employee_df[
            employee_df["Status"].str.contains(
                "Overtime",
                case=False,
                na=False
            )
        ]

        # ==========================================
        # File Name
        # ==========================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        report_name = (
            f"Attendance_Report_{timestamp}.xlsx"
        )

        report_path = os.path.join(

            self.report_folder,

            report_name

        )
        # ==========================================
        # Create Excel Workbook
        # ==========================================

        with pd.ExcelWriter(

            report_path,

            engine="openpyxl"

        ) as writer:

            # ======================================
            # Summary Sheet
            # ======================================

            summary_df.to_excel(

                writer,

                sheet_name="Summary",

                index=False

            )

            # ======================================
            # Employee Sheet
            # ======================================

            employee_df.to_excel(

                writer,

                sheet_name="Employees",

                index=False

            )

            # ======================================
            # Late Punch Sheet
            # ======================================

            late_df.to_excel(

                writer,

                sheet_name="Late Punch",

                index=False

            )

            # ======================================
            # Missing Punch In
            # ======================================

            missing_in_df.to_excel(

                writer,

                sheet_name="Missing Punch In",

                index=False

            )

            # ======================================
            # Missing Punch Out
            # ======================================

            missing_out_df.to_excel(

                writer,

                sheet_name="Missing Punch Out",

                index=False

            )

            # ======================================
            # Early Punch Out
            # ======================================

            early_df.to_excel(

                writer,

                sheet_name="Early Punch Out",

                index=False

            )

            # ======================================
            # Overtime
            # ======================================

            overtime_df.to_excel(

                writer,

                sheet_name="Overtime",

                index=False

            )

            workbook = writer.book

            # ======================================
            # Format Every Sheet
            # ======================================

            for sheet_name in workbook.sheetnames:

                sheet = workbook[sheet_name]

                # Header Style

                for cell in sheet[1]:

                    cell.fill = self.header_fill

                    cell.font = self.header_font

                    cell.alignment = self.center

                    cell.border = self.border

                # Data Style

                for row in sheet.iter_rows(min_row=2):

                    for cell in row:

                        cell.border = self.border

                        cell.alignment = self.center

                # Auto Column Width

                for column_cells in sheet.iter_cols():

                    length = max(
                        len(str(cell.value)) if cell.value else 0
                        for cell in column_cells
                    )

                    column_index = column_cells[0].column

                    sheet.column_dimensions[
                        get_column_letter(int(column_index))
                        
                    ].width = min(length + 5, 50)
                    # ======================================
            # Summary Sheet Formatting
            # ======================================

            summary_sheet = workbook["Summary"]

            summary_sheet.insert_rows(1, 4)

            summary_sheet["A1"] = COMPANY_NAME
            summary_sheet["A2"] = "Attendance Notification System Pro"
            summary_sheet["A3"] = "Daily Attendance Report"
            summary_sheet["A4"] = datetime.now().strftime(
                "Generated On : %d-%b-%Y %I:%M %p"
            )

            summary_sheet["A1"].font = Font(
                size=18,
                bold=True
            )

            summary_sheet["A2"].font = Font(
                size=14,
                bold=True
            )

            summary_sheet["A3"].font = Font(
                size=13,
                bold=True
            )

            summary_sheet["A4"].font = Font(
                italic=True
            )

            # ======================================
            # Color Summary Table
            # ======================================

            for cell in summary_sheet[5]:

                cell.fill = self.summary_fill

                cell.font = Font(
                    bold=True
                )

                cell.alignment = self.center

                cell.border = self.border

            for row in summary_sheet.iter_rows(
                min_row=6
            ):

                for cell in row:

                    cell.border = self.border

                    cell.alignment = self.center

            summary_sheet.freeze_panes = "A6"

            # ======================================
            # Freeze Employee Sheet
            # ======================================

            workbook["Employees"].freeze_panes = "A2"

            workbook["Late Punch"].freeze_panes = "A2"

            workbook["Missing Punch In"].freeze_panes = "A2"

            workbook["Missing Punch Out"].freeze_panes = "A2"

            workbook["Early Punch Out"].freeze_panes = "A2"

            workbook["Overtime"].freeze_panes = "A2"
            # ==========================================
        # Workbook Saved Automatically
        # ==========================================

        # ExcelWriter automatically saves the workbook
        # when exiting the 'with' block.

        # ==========================================
        # Return Report Path
        # ==========================================

        return report_path