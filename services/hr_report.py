"""
=========================================================
Attendance Notification System Pro
HR Report Generator
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""

from config import (
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING
)


class HRReportGenerator:
    """
    Enterprise HR Report Generator

    Features
    --------
    • Attendance Summary
    • Late Punch Report
    • Missing Punch Report
    • Monthly OT Report
    • High Performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.limit_text = f"{MONTHLY_OT_LIMIT}:00"

        self.warning_text = f"{MONTHLY_OT_WARNING}:00"

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

        hr.extend([

            "📊 ATTENDANCE SUMMARY",

            "",

            f"👥 Total Employees : {summary.get('total', 0)}",

            f"✅ Present : {summary.get('present', 0)}",

            f"⏰ Late Punch : {summary.get('late_in', 0)}",

            f"🏃 Early Out : {summary.get('early_out', 0)}",

            f"❌ Missing Punch In : {summary.get('missing_in', 0)}",

            f"❌ Missing Punch Out : {summary.get('missing_out', 0)}",

            f"🕒 Overtime Employees : {summary.get('overtime', 0)}",

            "",

            "=" * 60,

            ""

        ])

        # =====================================================
        # Employee Processing
        # =====================================================

        for employee in employees:

            emp_id = employee.get(

                "employee_id",

                ""

            )

            name = employee.get(

                "name",

                ""

            )

            monthly_ot = employee.get(

                "monthly_ot",

                "00:00"

            )

            monthly_status = employee.get(

                "monthly_status",

                "Normal"

            )

            status_list = employee.get(

                "status",

                []

            )

            # -----------------------------------------
            # Late Punch
            # -----------------------------------------

            if any(

                "Late" in status

                for status in status_list

            ):

                late.append(

                    f"⏰ {emp_id} - {name} ({employee.get('punch_in','--')})"

                )

            # -----------------------------------------
            # Missing Punch
            # -----------------------------------------

            if any(

                "Missing" in status

                for status in status_list

            ):

                late.append(

                    f"❌ {emp_id} - {name}"

                )

            # -----------------------------------------
            # Monthly OT Status
            # -----------------------------------------

            if monthly_status == "Warning":

                warning.append(

                    f"⚠️ {emp_id} - {name} : {monthly_ot}"

                )

            elif monthly_status == "Limit Reached":

                limit.append(

                    f"🟠 {emp_id} - {name} : {monthly_ot}"

                )

            elif monthly_status == "Exceeded":

                exceeded.append(

                    f"🔴 {emp_id} - {name} : {monthly_ot}"

                )
                # =====================================================
        # Monthly OT Warning
        # =====================================================

        if warning:

            hr.append(

                f"⚠️ MONTHLY OT WARNING ({self.warning_text})"

            )

            hr.extend(

                warning

            )

            hr.append("")

        # =====================================================
        # Monthly OT Limit Reached
        # =====================================================

        if limit:

            hr.append(

                f"🟠 MONTHLY OT LIMIT REACHED ({self.limit_text})"

            )

            hr.extend(

                limit

            )

            hr.append("")

        # =====================================================
        # Monthly OT Exceeded
        # =====================================================

        if exceeded:

            hr.append(

                "🔴 MONTHLY OT EXCEEDED"

            )

            hr.extend(

                exceeded

            )

            hr.append("")

        # =====================================================
        # Late & Missing Punch Report
        # =====================================================

        if late:

            late.insert(

                0,

                "⏰ LATE & MISSING PUNCH REPORT"

            )

            late.insert(

                1,

                ""

            )

        else:

            late.extend([

                "⏰ LATE & MISSING PUNCH REPORT",

                "",

                "No late or missing punch records found."

            ])

        # =====================================================
        # Generate Reports
        # =====================================================

        hr_report = "\n".join(

            hr

        )

        late_punch_report = "\n".join(

            late

        )

        print("=" * 60)
        print("HR Report Generated Successfully")
        print("=" * 60)

        return {

            "hr_report": hr_report,

            "late_punch_report": late_punch_report

        }
                