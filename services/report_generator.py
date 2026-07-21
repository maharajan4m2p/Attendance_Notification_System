"""
=========================================================
Attendance Notification System Pro
Report Generator
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

import os

from datetime import datetime

import pandas as pd

from config import (
    REPORT_FOLDER,
    MONTHLY_OT_LIMIT
)


class ReportGenerator:

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
    # Generate Excel Report
    # =====================================================

    def generate_excel(
        self,
        employees,
        filename="Attendance_Report.xlsx"
    ):

        report_data = []

        for emp in employees:

            remaining = (
                MONTHLY_OT_LIMIT * 60
            ) - emp.get(
                "monthly_ot_minutes",
                0
            )

            if remaining < 0:
                remaining = 0

            remaining_hours = (
                f"{remaining//60:02d}:{remaining%60:02d}"
            )

            report_data.append({

                "Employee ID": emp["employee_id"],

                "Employee Name": emp["name"],

                "Department": emp["department"],

                "Designation": emp["designation"],

                "Attendance Date": emp["attendance_date"],

                "Punch In": emp["punch_in"],

                "Punch Out": emp["punch_out"],

                "Daily OT": emp["daily_ot"],

                "Monthly OT": emp["monthly_ot"],

                "Remaining OT": remaining_hours,

                "Daily Status": emp["daily_ot_status"],

                "Monthly Status": emp["monthly_status"],

                "Notification": emp["notification"]

            })

        dataframe = pd.DataFrame(report_data)

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filepath = os.path.join(
            self.report_folder,
            f"{timestamp}_{filename}"
        )

        with pd.ExcelWriter(
            filepath,
            engine="openpyxl"
        ) as writer:

            dataframe.to_excel(
                writer,
                sheet_name="Attendance Report",
                index=False
            )

            worksheet = writer.sheets["Attendance Report"]

            # =====================================
            # Auto Fit Columns
            # =====================================

            for column_cells in worksheet.columns:

                length = max(
                    len(str(cell.value))
                    if cell.value is not None
                    else 0
                    for cell in column_cells
                )

                worksheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = min(
                    length + 5,
                    50
                )

        return filepath

    # =====================================================
    # Compatibility Wrapper
    # =====================================================

    def generate_report(
        self,
        result,
        filename="Attendance_Report.xlsx"
    ):

        return self.generate_excel(
            result["employees"],
            filename
        )