"""
=========================================================
Attendance Notification System Pro
Enterprise HR Report Generator
Version : 14.0 Enterprise
=========================================================
"""

from datetime import datetime

from config import (
    COMPANY_NAME,
    NORMAL_STATUS,
    WARNING_STATUS,
    LIMIT_REACHED_STATUS,
    EXCEEDED_STATUS
)


class HRReportGenerator:
    """
    Enterprise HR Report Generator

    Generates

        • HR Report
        • Late Punch Report
        • WhatsApp HR Report
        • Dashboard Report
        • Monthly OT Summary
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.company = COMPANY_NAME

        self.separator = "=" * 80

        self.generated_time = datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

    # =====================================================
    # Helper
    # =====================================================

    def get_value(
        self,
        employee,
        key,
        default=""
    ):

        value = employee.get(
            key,
            default
        )

        if value is None:

            return default

        return value

    # =====================================================
    # Generate Reports
    # =====================================================

    def generate(
        self,
        employees,
        summary
    ):

        report = []

        report.append(self.separator)
        report.append(self.company)
        report.append("ENTERPRISE DAILY ATTENDANCE REPORT")
        report.append(self.separator)

        report.append(
            f"Generated On : {self.generated_time}"
        )

        report.append("")
        # =====================================================
        # HR Report Header
        # =====================================================

        report = []

        report.append(self.separator)
        report.append(self.company)
        report.append("ENTERPRISE DAILY ATTENDANCE REPORT")
        report.append(self.separator)

        report.append(
            f"Generated On : {self.generated_time}"
        )

        report.append("")

        # =====================================================
        # Attendance Summary
        # =====================================================

        report.append("ATTENDANCE SUMMARY")
        report.append("-" * 80)

        report.append(
            f"Total Employees          : {summary.get('total',0)}"
        )

        report.append(
            f"Present                  : {summary.get('present',0)}"
        )

        report.append(
            f"Absent                   : {summary.get('absent',0)}"
        )

        report.append(
            f"Half Day                 : {summary.get('half_day',0)}"
        )

        report.append(
            f"Late Punch               : {summary.get('late_in',0)}"
        )

        report.append(
            f"Early Out                : {summary.get('early_out',0)}"
        )

        report.append(
            f"Missing Punch In         : {summary.get('missing_in',0)}"
        )

        report.append(
            f"Missing Punch Out        : {summary.get('missing_out',0)}"
        )

        report.append(
            f"Employees With OT        : {summary.get('overtime',0)}"
        )

        report.append(
            f"Monthly Warning          : {summary.get('monthly_warning',0)}"
        )

        report.append(
            f"Monthly Limit Reached    : {summary.get('monthly_limit_reached',0)}"
        )

        report.append(
            f"Monthly OT Exceeded      : {summary.get('monthly_ot_exceeded',0)}"
        )

        # =====================================================
        # Monthly OT Statistics
        # =====================================================

        total_monthly_minutes = sum(

            int(
                employee.get(
                    "monthly_ot_minutes",
                    0
                )
            )

            for employee in employees

        )

        total_remaining_minutes = sum(

            int(
                employee.get(
                    "remaining_ot_minutes",
                    0
                )
            )

            for employee in employees

        )

        total_ot_hours = total_monthly_minutes // 60
        total_ot_minutes = total_monthly_minutes % 60

        remaining_hours = total_remaining_minutes // 60
        remaining_minutes = total_remaining_minutes % 60

        report.append("")

        report.append("MONTHLY OT SUMMARY")
        report.append("-" * 80)

        report.append(
            f"Total Monthly OT         : {total_ot_hours:02d}:{total_ot_minutes:02d}"
        )

        report.append(
            f"Remaining OT             : {remaining_hours:02d}:{remaining_minutes:02d}"
        )

        report.append("")

        warning_count = sum(

            1

            for employee in employees

            if employee.get(
                "monthly_status"
            ) == WARNING_STATUS

        )

        limit_count = sum(

            1

            for employee in employees

            if employee.get(
                "monthly_status"
            ) == LIMIT_REACHED_STATUS

        )

        exceeded_count = sum(

            1

            for employee in employees

            if employee.get(
                "monthly_status"
            ) == EXCEEDED_STATUS

        )

        normal_count = sum(

            1

            for employee in employees

            if employee.get(
                "monthly_status"
            ) == NORMAL_STATUS

        )

        report.append(
            f"Normal Employees         : {normal_count}"
        )

        report.append(
            f"Warning Employees        : {warning_count}"
        )

        report.append(
            f"Limit Reached Employees  : {limit_count}"
        )

        report.append(
            f"Exceeded Employees       : {exceeded_count}"
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
                f"{number}. Employee ID      : {self.get_value(employee,'employee_id')}"
            )

            report.append(
                f"   Employee Name    : {self.get_value(employee,'name')}"
            )

            report.append(
                f"   Department       : {self.get_value(employee,'department')}"
            )

            report.append(
                f"   Designation      : {self.get_value(employee,'designation')}"
            )

            report.append(
                f"   Attendance Date  : {self.get_value(employee,'attendance_date')}"
            )

            report.append(
                f"   Punch In         : {self.get_value(employee,'punch_in','--')}"
            )

            report.append(
                f"   Punch Out        : {self.get_value(employee,'punch_out','--')}"
            )

            report.append(
                f"   Daily OT         : {self.get_value(employee,'daily_ot','00:00')}"
            )

            report.append(
                f"   Monthly OT       : {self.get_value(employee,'monthly_ot','00:00')}"
            )

            report.append(
                f"   Remaining OT     : {self.get_value(employee,'remaining_ot','25:00')}"
            )

            report.append(
                f"   Monthly Status   : {self.get_value(employee,'monthly_status',NORMAL_STATUS)}"
            )

            report.append(
                f"   Daily Status     : {self.get_value(employee,'daily_status','')}"
            )

            report.append(
                f"   Notification     : {self.get_value(employee,'notification','')}"
            )

            # =====================================================
            # Daily OT History
            # =====================================================

            report.append("")
            report.append("   Daily OT History")
            report.append("   " + "-" * 60)

            line = []

            for day in range(1, 32):

                value = employee.get(
                    f"Day{day}",
                    "00:00"
                )

                line.append(
                    f"D{day}:{value}"
                )

                if len(line) == 7:

                    report.append(
                        "   " + " | ".join(line)
                    )

                    line = []

            if line:

                report.append(
                    "   " + " | ".join(line)
                )

            # =====================================================
            # Remarks
            # =====================================================

            status = employee.get(
                "status",
                []
            )

            if status:

                report.append("")

                report.append(
                    "   Remarks          : "
                    + ", ".join(status)
                )

            report.append(
                "-" * 80
            )

        hr_report = "\n".join(
            report
        )
        # =====================================================
        # Late Punch Report
        # =====================================================

        late_report = []

        late_report.append(self.separator)
        late_report.append(self.company)
        late_report.append("ENTERPRISE LATE PUNCH REPORT")
        late_report.append(self.separator)

        late_report.append(
            f"Generated On : {self.generated_time}"
        )

        late_report.append("")

        late_count = 0

        for employee in employees:

            status_list = employee.get(
                "status",
                []
            )

            if any(
                "Late Punch" in status
                for status in status_list
            ):

                late_count += 1

                late_report.append(
                    f"{late_count}. Employee ID : {self.get_value(employee,'employee_id')}"
                )

                late_report.append(
                    f"   Name           : {self.get_value(employee,'name')}"
                )

                late_report.append(
                    f"   Department     : {self.get_value(employee,'department')}"
                )

                late_report.append(
                    f"   Punch In       : {self.get_value(employee,'punch_in','--')}"
                )

                late_report.append(
                    f"   Daily OT       : {self.get_value(employee,'daily_ot','00:00')}"
                )

                late_report.append(
                    f"   Monthly OT     : {self.get_value(employee,'monthly_ot','00:00')}"
                )

                late_report.append(
                    f"   Monthly Status : {self.get_value(employee,'monthly_status',NORMAL_STATUS)}"
                )

                late_report.append("-" * 80)

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

        whatsapp.append(
            f"👥 Total Employees : {summary.get('total',0)}"
        )

        whatsapp.append(
            f"✅ Present : {summary.get('present',0)}"
        )

        whatsapp.append(
            f"❌ Absent : {summary.get('absent',0)}"
        )

        whatsapp.append(
            f"🟡 Half Day : {summary.get('half_day',0)}"
        )

        whatsapp.append(
            f"⏰ Late Punch : {summary.get('late_in',0)}"
        )

        whatsapp.append(
            f"🏃 Early Out : {summary.get('early_out',0)}"
        )

        whatsapp.append(
            f"🚫 Missing IN : {summary.get('missing_in',0)}"
        )

        whatsapp.append(
            f"🚫 Missing OUT : {summary.get('missing_out',0)}"
        )

        whatsapp.append(
            f"🕒 OT Employees : {summary.get('overtime',0)}"
        )

        whatsapp.append(
            f"⚠ Warning : {summary.get('monthly_warning',0)}"
        )

        whatsapp.append(
            f"🟠 Limit Reached : {summary.get('monthly_limit_reached',0)}"
        )

        whatsapp.append(
            f"🔴 Exceeded : {summary.get('monthly_ot_exceeded',0)}"
        )

        whatsapp.append("")

        issue_count = 0

        for employee in employees:

            if employee.get("status") != ["On Time"]:

                issue_count += 1

                whatsapp.append(
                    f"{issue_count}. {self.get_value(employee,'employee_id')} - {self.get_value(employee,'name')}"
                )

                whatsapp.append(
                    f"Status : {', '.join(employee.get('status', []))}"
                )

                whatsapp.append(
                    f"Monthly OT : {self.get_value(employee,'monthly_ot','00:00')}"
                )

                whatsapp.append(
                    f"Remaining OT : {self.get_value(employee,'remaining_ot','25:00')}"
                )

                whatsapp.append("")

        whatsapp.append("Generated by Attendance Notification System Pro")

        whatsapp_hr_report = "\n".join(
            whatsapp
        )
        # =====================================================
        # Top Monthly OT Employees
        # =====================================================

        top_monthly_ot = sorted(

            employees,

            key=lambda employee: int(
                employee.get(
                    "monthly_ot_minutes",
                    0
                )
            ),

            reverse=True

        )[:10]

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
            ),

            "top_monthly_ot": [

                {

                    "employee_id": employee.get(
                        "employee_id",
                        ""
                    ),

                    "name": employee.get(
                        "name",
                        ""
                    ),

                    "department": employee.get(
                        "department",
                        ""
                    ),

                    "monthly_ot": employee.get(
                        "monthly_ot",
                        "00:00"
                    ),

                    "remaining_ot": employee.get(
                        "remaining_ot",
                        "25:00"
                    ),

                    "monthly_status": employee.get(
                        "monthly_status",
                        NORMAL_STATUS
                    )

                }

                for employee in top_monthly_ot

            ]

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