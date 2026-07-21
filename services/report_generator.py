"""
=========================================================
Attendance Notification System Pro
Report Generator
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""

import os

import pandas as pd

from openpyxl import load_workbook

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment
)

from config import REPORT_FOLDER


class ReportGenerator:

    """
    Enterprise Excel Report Generator

    Features
    --------
    • High Speed Excel Export
    • Auto Column Width
    • Status Highlighting
    • Freeze Header
    • Auto Filter
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        os.makedirs(

            REPORT_FOLDER,

            exist_ok=True

        )

        self.header_fill = PatternFill(

            fill_type="solid",

            start_color="1F4E78",

            end_color="1F4E78"

        )

        self.header_font = Font(

            bold=True,

            color="FFFFFF"

        )

        self.center_alignment = Alignment(

            horizontal="center",

            vertical="center"

        )

        self.green_fill = PatternFill(

            fill_type="solid",

            start_color="C6EFCE",

            end_color="C6EFCE"

        )

        self.yellow_fill = PatternFill(

            fill_type="solid",

            start_color="FFF2CC",

            end_color="FFF2CC"

        )

        self.red_fill = PatternFill(

            fill_type="solid",

            start_color="F4CCCC",

            end_color="F4CCCC"

        )

    # =====================================================
    # Generate Excel Report
    # =====================================================

    def generate_excel(

        self,

        employees,

        filename

    ):

        if not employees:

            raise ValueError(

                "No employee data available."

            )

        report_path = os.path.join(

            REPORT_FOLDER,

            filename

        )

        print("=" * 60)
        print("Generating Excel Report...")
        print("=" * 60)

        dataframe = pd.DataFrame(

            employees

        )

        dataframe.to_excel(

            report_path,

            index=False,

            engine="openpyxl"

        )

        workbook = load_workbook(

            report_path

        )

        workbook = load_workbook(report_path)
        
        worksheet = workbook.active
        
        if worksheet is None:
            raise ValueError("Worksheet not found")
        
        worksheet.title = "Attendance Report"

        # =====================================================
        # Header Formatting
        # =====================================================

        for cell in worksheet[1]:

            cell.fill = self.header_fill

            cell.font = self.header_font

            cell.alignment = self.center_alignment
        
        if worksheet is not None:
            worksheet.freeze_panes = "A2"
        # =====================================================
        # Auto Column Width
        # =====================================================
        if worksheet is None:
            raise ValueError("Worksheet is not found")
        
        for column_cells in worksheet.columns:

            max_length = 0

            from openpyxl.cell.cell import Cell
            
            first_cell = column_cells[0]
            
            if isinstance(first_cell,Cell):
                column_letter = first_cell.column_letter
            else:
                continue

            for cell in column_cells:

                try:

                    if cell.value is not None:

                        max_length = max(

                            max_length,

                            len(str(cell.value))

                        )

                except Exception:

                    pass
            if workbook is not None:
                
                worksheet.column_dimensions[
                    column_letter
                ].width = min(

                    max_length + 3,

                    40

                )

        # =====================================================
        # Status Cell Coloring
        # =====================================================
        if worksheet is not None:
            for row in worksheet.iter_rows(

                min_row=2

            ):

                for cell in row:

                    value = str(

                        cell.value

                    ).strip()

                    if value == "Normal":

                        cell.fill = self.green_fill

                    elif value in (

                        "Warning",

                        "Limit Reached"

                    ):

                        cell.fill = self.yellow_fill

                    elif value == "Exceeded":

                        cell.fill = self.red_fill

                    cell.alignment = self.center_alignment

        # =====================================================
        # Auto Filter
        # =====================================================
        if worksheet is not None:
            worksheet.auto_filter.ref = worksheet.dimensions

        # =====================================================
        # Save Workbook
        # =====================================================

        workbook.save(

            report_path

        )

        workbook.close()

        print("=" * 60)
        print("Excel Report Generated Successfully")
        print("=" * 60)

        return report_path