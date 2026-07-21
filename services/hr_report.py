"""
=========================================================
Attendance Notification System Pro
HR Report Generator
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""

from config import (
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING
)


class HRReportGenerator:

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.monthly_limit = MONTHLY_OT_LIMIT

        self.warning_limit = MONTHLY_OT_WARNING
        # =====================================================
    # Generate HR Report
    # =====================================================

    def generate(
        self,
        employees,
        summary
    ):

        hr = []

        late = []

        warning = []

        limit = []

        exceeded = []

        # =====================================================
        # Attendance Summary
        # =====================================================

        hr.append("=" * 60)

        hr.append("ATTENDANCE SUMMARY REPORT")

        hr.append("=" * 60)

        hr.append("")

        hr.append(
            f"Total Employees      : {summary.get('total', 0)}"
        )

        hr.append(
            f"Present Employees    : {summary.get('present', 0)}"
        )

        hr.append(
            f"Late Punch           : {summary.get('late_in', 0)}"
        )

        hr.append(
            f"Early Out            : {summary.get('early_out', 0)}"
        )

        hr.append(
            f"Missing Punch In     : {summary.get('missing_in', 0)}"
        )

        hr.append(
            f"Missing Punch Out    : {summary.get('missing_out', 0)}"
        )

        hr.append(
            f"Overtime Employees   : {summary.get('overtime', 0)}"
        )

        hr.append(
            f"OT Warning           : {summary.get('warning', 0)}"
        )

        hr.append(
            f"Limit Reached        : {summary.get('limit_reached', 0)}"
        )

        hr.append(
            f"OT Exceeded          : {summary.get('monthly_ot_exceeded', 0)}"
        )

        hr.append("")

        hr.append("=" * 60)

        hr.append("")
        # =====================================================
        # Process Employees
        # =====================================================

        for emp in employees:

            name = emp.get(
                "name",
                ""
            )

            emp_id = emp.get(
                "employee_id",
                ""
            )

            department = emp.get(
                "department",
                ""
            )

            monthly_ot = emp.get(
                "monthly_ot",
                "00:00"
            )

            status = emp.get(
                "monthly_status",
                "Normal"
            )

            employee_status = emp.get(
                "status",
                []
            )

            # -----------------------------------------
            # Late Punch
            # -----------------------------------------

            if any(
                "Late" in item
                for item in employee_status
            ):

                late.append(

                    f"{emp_id} | {name} | {department} | "
                    f"Punch In : {emp.get('punch_in', '--')}"

                )

            # -----------------------------------------
            # Missing Punch
            # -----------------------------------------

            if any(
                "Missing" in item
                for item in employee_status
            ):

                late.append(

                    f"{emp_id} | {name} | Missing Punch"

                )

            # -----------------------------------------
            # Monthly Warning
            # -----------------------------------------

            if status == "Warning":

                warning.append(

                    f"{emp_id} | {name} | OT : {monthly_ot}"

                )

            # -----------------------------------------
            # Monthly Limit Reached
            # -----------------------------------------

            elif status == "Limit Reached":

                limit.append(

                    f"{emp_id} | {name} | OT : {monthly_ot}"

                )

            # -----------------------------------------
            # Monthly Exceeded
            # -----------------------------------------

            elif status == "Exceeded":

                exceeded.append(

                    f"{emp_id} | {name} | OT : {monthly_ot}"

                )

        # =====================================================
        # Warning Section
        # =====================================================

        if warning:

            hr.append("MONTHLY OT WARNING")

            hr.append("-" * 60)

            hr.extend(warning)

            hr.append("")

        # =====================================================
        # Limit Reached Section
        # =====================================================

        if limit:

            hr.append("MONTHLY OT LIMIT REACHED")

            hr.append("-" * 60)

            hr.extend(limit)

            hr.append("")

        # =====================================================
        # Exceeded Section
        # =====================================================

        if exceeded:

            hr.append("MONTHLY OT EXCEEDED")

            hr.append("-" * 60)

            hr.extend(exceeded)

            hr.append("")

        # =====================================================
        # Late Punch Section
        # =====================================================

        if late:

            hr.append("LATE / MISSING PUNCH REPORT")

            hr.append("-" * 60)

            hr.extend(late)

            hr.append("")
            # =====================================================
        # Footer
        # =====================================================

        hr.append("=" * 60)

        hr.append(
            "Attendance Notification System Pro"
        )

        hr.append("HR Report Generator")

        hr.append("=" * 60)

        # =====================================================
        # Generate Report Strings
        # =====================================================

        hr_report = "\n".join(hr)

        late_punch_report = "\n".join(late)

        # =====================================================
        # Return Reports
        # =====================================================

        return {

            "hr_report": hr_report,

            "late_punch_report": late_punch_report

        }