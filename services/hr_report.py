"""
=========================================================
Attendance Notification System Pro
Enterprise HR Report Generator
Version : 13.0 Enterprise
=========================================================
"""

from datetime import datetime

from config import COMPANY_NAME


class HRReportGenerator:
    """
    Enterprise HR Report Generator
    Generates:
        • HR Report
        • Late Punch Report
        • WhatsApp Report
        • Dashboard Summary
    """

    def __init__(self):

        self.company = COMPANY_NAME

        self.separator = "=" * 70

        self.generated_time = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )
        # =====================================================
    # Generate Reports
    # =====================================================

    def generate(
        self,
        employees,
        summary
    ):

        # -----------------------------------------
        # HR Report Header
        # -----------------------------------------

        report = []

        report.append(self.separator)
        report.append(self.company)
        report.append("DAILY ATTENDANCE REPORT")
        report.append(self.separator)

        report.append(
            f"Generated On : {self.generated_time}"
        )

        report.append("")

        # -----------------------------------------
        # Attendance Summary
        # -----------------------------------------

        report.append("ATTENDANCE SUMMARY")
        report.append("-" * 70)

        report.append(
            f"Total Employees        : {summary.get('total', 0)}"
        )

        report.append(
            f"Present                : {summary.get('present', 0)}"
        )

        report.append(
            f"Absent                 : {summary.get('absent', 0)}"
        )

        report.append(
            f"Half Day               : {summary.get('half_day', 0)}"
        )

        report.append(
            f"Late Punch             : {summary.get('late_in', 0)}"
        )

        report.append(
            f"Early Out              : {summary.get('early_out', 0)}"
        )

        report.append(
            f"Missing Punch In       : {summary.get('missing_in', 0)}"
        )

        report.append(
            f"Missing Punch Out      : {summary.get('missing_out', 0)}"
        )

        report.append(
            f"Overtime Employees     : {summary.get('overtime', 0)}"
        )

        report.append(
            f"Monthly OT Warning     : {summary.get('monthly_warning', 0)}"
        )

        report.append(
            f"Monthly Limit Reached  : {summary.get('monthly_limit_reached', 0)}"
        )

        report.append(
            f"Monthly OT Exceeded    : {summary.get('monthly_ot_exceeded', 0)}"
        )

        report.append("")

        report.append(self.separator)

        report.append("EMPLOYEE DETAILS")

        report.append(self.separator)

        report.append("")
        # =====================================================
        # Employee Details
        # =====================================================

        for number, employee in enumerate(
            employees,
            start=1
        ):

            report.append(
                f"{number}. Employee ID      : {employee.get('employee_id', '')}"
            )

            report.append(
                f"   Employee Name    : {employee.get('name', '')}"
            )

            report.append(
                f"   Department       : {employee.get('department', '')}"
            )

            report.append(
                f"   Designation      : {employee.get('designation', '')}"
            )

            report.append(
                f"   Attendance Date  : {employee.get('attendance_date', '')}"
            )

            report.append(
                f"   Punch In         : {employee.get('punch_in', '--')}"
            )

            report.append(
                f"   Punch Out        : {employee.get('punch_out', '--')}"
            )

            report.append(
                f"   Daily OT         : {employee.get('daily_ot', '00:00')}"
            )

            report.append(
                f"   Monthly OT       : {employee.get('monthly_ot', '00:00')}"
            )

            report.append(
                f"   Remaining OT     : {employee.get('remaining_ot', '25:00')}"
            )

            report.append(
                f"   Monthly Status   : {employee.get('monthly_status', 'Normal')}"
            )

            report.append(
                f"   Daily Status     : {employee.get('daily_status', 'Normal')}"
            )

            report.append(
                f"   Notification     : {employee.get('notification', '')}"
            )

            status = employee.get(
                "status",
                []
            )

            if status:

                report.append(
                    "   Remarks          : "
                    + ", ".join(status)
                )

            report.append(
                "-" * 70
            )

        hr_report = "\n".join(report)
        # =====================================================
        # Late Punch Report
        # =====================================================

        late_report = []

        late_report.append(self.separator)
        late_report.append(self.company)
        late_report.append("LATE PUNCH REPORT")
        late_report.append(self.separator)
        late_report.append(f"Generated On : {self.generated_time}")
        late_report.append("")

        late_count = 0

        for employee in employees:

            for status in employee.get("status", []):

                if "Late Punch" in status:

                    late_count += 1

                    late_report.append(
                        f"{late_count}. {employee.get('employee_id', '')}"
                    )

                    late_report.append(
                        f"   Name        : {employee.get('name', '')}"
                    )

                    late_report.append(
                        f"   Department  : {employee.get('department', '')}"
                    )

                    late_report.append(
                        f"   Punch In    : {employee.get('punch_in', '--')}"
                    )

                    late_report.append(
                        f"   Status      : {status}"
                    )

                    late_report.append("-" * 70)

        if late_count == 0:

            late_report.append(
                "No employees have late punch today."
            )

        late_punch_report = "\n".join(
            late_report
        )

        # =====================================================
        # WhatsApp HR Report
        # =====================================================

        whatsapp = []

        whatsapp.append(f"🏢 {self.company}")
        whatsapp.append("")
        whatsapp.append("📋 DAILY ATTENDANCE REPORT")
        whatsapp.append("")
        whatsapp.append(f"📅 {self.generated_time}")
        whatsapp.append("")

        whatsapp.append(f"👥 Total Employees : {summary.get('total',0)}")
        whatsapp.append(f"✅ Present : {summary.get('present',0)}")
        whatsapp.append(f"❌ Absent : {summary.get('absent',0)}")
        whatsapp.append(f"🟡 Half Day : {summary.get('half_day',0)}")
        whatsapp.append(f"⏰ Late Punch : {summary.get('late_in',0)}")
        whatsapp.append(f"🏃 Early Out : {summary.get('early_out',0)}")
        whatsapp.append(f"🚫 Missing IN : {summary.get('missing_in',0)}")
        whatsapp.append(f"🚫 Missing OUT : {summary.get('missing_out',0)}")
        whatsapp.append(f"🕒 OT Employees : {summary.get('overtime',0)}")
        whatsapp.append("")

        if employees:

            whatsapp.append("📌 Employees With Issues")

            for employee in employees:

                if employee.get("status") != ["On Time"]:

                    whatsapp.append("")

                    whatsapp.append(
                        f"{employee.get('employee_id','')} - {employee.get('name','')}"
                    )

                    whatsapp.append(
                        ", ".join(employee.get("status", []))
                    )

        whatsapp.append("")
        whatsapp.append("Generated by Attendance Notification System Pro")

        whatsapp_hr_report = "\n".join(
            whatsapp
        )
        # =====================================================
        # Dashboard Report
        # =====================================================

        dashboard_report = {

            "company": self.company,

            "generated_on": self.generated_time,

            "total": summary.get(
                "total",
                0
            ),

            "present": summary.get(
                "present",
                0
            ),

            "absent": summary.get(
                "absent",
                0
            ),

            "half_day": summary.get(
                "half_day",
                0
            ),

            "late_in": summary.get(
                "late_in",
                0
            ),

            "early_out": summary.get(
                "early_out",
                0
            ),

            "missing_in": summary.get(
                "missing_in",
                0
            ),

            "missing_out": summary.get(
                "missing_out",
                0
            ),

            "overtime": summary.get(
                "overtime",
                0
            ),

            "monthly_warning": summary.get(
                "monthly_warning",
                0
            ),

            "monthly_limit_reached": summary.get(
                "monthly_limit_reached",
                0
            ),

            "monthly_ot_exceeded": summary.get(
                "monthly_ot_exceeded",
                0
            )

        }

        # =====================================================
        # Return Reports
        # =====================================================

        return {

            "hr_report": hr_report,

            "late_punch_report": late_punch_report,

            "whatsapp_hr_report": whatsapp_hr_report,

            "dashboard_report": dashboard_report

        }