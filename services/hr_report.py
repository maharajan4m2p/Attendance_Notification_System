"""
=========================================================
Attendance Notification System Pro
HR Report Generator
Version : 10.0 Enterprise
=========================================================
"""

from config import (
    COMPANY_NAME,
    MONTHLY_OT_LIMIT,
    MONTHLY_OT_WARNING
)


class HRReportGenerator:
    """
    Enterprise HR Report Generator

    Features
    --------
    • Daily Attendance Summary
    • Late Punch Report
    • Missing Punch Report
    • Monthly Overtime Report
    • HR WhatsApp Report
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.company = COMPANY_NAME

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
        # Company Header
        # =====================================================

        hr.extend([

            f"🏢 {self.company}",

            "📋 DAILY ATTENDANCE REPORT",

            "",

            "=" * 60,

            ""

        ])

        # =====================================================
        # Attendance Summary
        # =====================================================

        hr.extend([

            "📊 ATTENDANCE SUMMARY",

            "",

            f"👥 Total Employees      : {summary.get('total', 0)}",

            f"✅ Present              : {summary.get('present', 0)}",

            f"⏰ Late Punch           : {summary.get('late_in', 0)}",

            f"🏃 Early Out            : {summary.get('early_out', 0)}",

            f"❌ Missing Punch In     : {summary.get('missing_in', 0)}",

            f"❌ Missing Punch Out    : {summary.get('missing_out', 0)}",

            f"🕒 Overtime Employees   : {summary.get('overtime', 0)}",

            f"⚠️ OT Warning          : {summary.get('warning', 0)}",

            f"🟠 Limit Reached       : {summary.get('limit_reached', 0)}",

            f"🔴 OT Exceeded         : {summary.get('exceeded', 0)}",

            "",

            "=" * 60,

            ""

        ])
        # =====================================================
        # Employee Processing
        # =====================================================

        for emp in employees:

            emp_id = str(
                emp.get(
                    "employee_id",
                    ""
                )
            )

            name = str(
                emp.get(
                    "name",
                    ""
                )
            )

            department = str(
                emp.get(
                    "department",
                    ""
                )
            )

            punch_in = emp.get(
                "punch_in",
                "--"
            )

            punch_out = emp.get(
                "punch_out",
                "--"
            )

            daily_ot = emp.get(
                "daily_ot",
                "00:00"
            )

            monthly_ot = emp.get(
                "monthly_ot",
                "00:00"
            )

            monthly_status = emp.get(
                "monthly_status",
                "Normal"
            )

            status_list = emp.get(
                "status",
                []
            )

            # -----------------------------------------
            # Late Punch
            # -----------------------------------------

            if any(
                "Late" in str(status)
                for status in status_list
            ):

                late.append(

                    f"⏰ {emp_id} | {name} | {department} | IN : {punch_in}"

                )

            # -----------------------------------------
            # Missing Punch
            # -----------------------------------------

            if any(
                "Missing" in str(status)
                for status in status_list
            ):

                late.append(

                    f"❌ {emp_id} | {name} | OUT : {punch_out}"

                )

            # -----------------------------------------
            # Monthly OT Warning
            # -----------------------------------------

            if monthly_status == "Warning":

                warning.append(

                    f"⚠️ {emp_id} | {name} | OT : {monthly_ot}"

                )

            # -----------------------------------------
            # Monthly OT Limit Reached
            # -----------------------------------------

            elif monthly_status == "Limit Reached":

                limit.append(

                    f"🟠 {emp_id} | {name} | OT : {monthly_ot}"

                )

            # -----------------------------------------
            # Monthly OT Exceeded
            # -----------------------------------------

            elif monthly_status == "Exceeded":

                exceeded.append(

                    f"🔴 {emp_id} | {name} | OT : {monthly_ot}"

                )
                # =====================================================
        # Monthly OT Warning
        # =====================================================

        if warning:

            hr.extend([

                f"⚠️ MONTHLY OT WARNING ({self.warning_text})",

                ""

            ])

            hr.extend(warning)

            hr.append("")

        # =====================================================
        # Monthly OT Limit Reached
        # =====================================================

        if limit:

            hr.extend([

                f"🟠 MONTHLY OT LIMIT REACHED ({self.limit_text})",

                ""

            ])

            hr.extend(limit)

            hr.append("")

        # =====================================================
        # Monthly OT Exceeded
        # =====================================================

        if exceeded:

            hr.extend([

                "🔴 MONTHLY OT EXCEEDED",

                ""

            ])

            hr.extend(exceeded)

            hr.append("")

        # =====================================================
        # No Monthly OT Issues
        # =====================================================

        if not warning and not limit and not exceeded:

            hr.extend([

                "✅ MONTHLY OT STATUS",

                "",

                "No employees have crossed the monthly overtime warning limit.",

                ""

            ])

        # =====================================================
        # Late / Missing Punch Report
        # =====================================================

        if late:

            hr.extend([

                "=" * 60,

                "",

                "⏰ LATE & MISSING PUNCH REPORT",

                ""

            ])

            hr.extend(late)

            hr.append("")

        else:

            hr.extend([

                "=" * 60,

                "",

                "⏰ LATE & MISSING PUNCH REPORT",

                "",

                "✅ No late or missing punch records found.",

                ""

            ])
            # =====================================================
        # Report Footer
        # =====================================================

        hr.extend([

            "=" * 60,

            "",

            "Attendance Notification System Pro",

            "Generated Automatically",

            ""

        ])

        # =====================================================
        # Generate Final Reports
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

            "late_punch_report": late_punch_report,

            "warning_report": "\n".join(warning),

            "limit_report": "\n".join(limit),

            "exceeded_report": "\n".join(exceeded),

            "warning_count": len(warning),

            "limit_count": len(limit),

            "exceeded_count": len(exceeded),

            "late_count": len(late)

        }