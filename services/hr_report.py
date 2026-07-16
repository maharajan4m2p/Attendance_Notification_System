"""
=========================================
HR Report Generator
Developed by Maharajan
=========================================
"""

from datetime import datetime


class HRReportGenerator:

    # =====================================================
    # Generate HR Reports
    # =====================================================

    def generate(self, employees, summary):

        # ==========================================
        # Create Reports
        # ==========================================

        hr_report = []

        late_report = []

        today = datetime.now().strftime("%d-%b-%Y")

        current_time = datetime.now().strftime("%I:%M %p")

        present = (
            summary["total"]
            - summary["missing_in"]
        )

        # ==========================================
        # HR REPORT HEADER
        # ==========================================

        hr_report.append(
            "══════════════════════════════════════"
        )

        hr_report.append(
            "🏢 ADISTHAM VENTURES PRIVATE LIMITED"
        )

        hr_report.append(
            "📢 DAILY ATTENDANCE REPORT"
        )

        hr_report.append(
            f"📅 Date : {today}"
        )

        hr_report.append(
            f"🕒 Generated : {current_time}"
        )

        hr_report.append(
            "══════════════════════════════════════"
        )

        hr_report.append("")

        # ==========================================
        # SUMMARY
        # ==========================================

        hr_report.append(
            "📊 SUMMARY"
        )

        hr_report.append("")

        hr_report.append(
            f"👥 Total Employees : {summary['total']}"
        )

        hr_report.append(
            f"🟢 Present : {present}"
        )

        hr_report.append(
            f"🔴 Late Punch : {summary['late_in']}"
        )

        hr_report.append(
            f"🟠 Early Punch Out : {summary['early_out']}"
        )

        hr_report.append(
            f"❌ Missing Punch In : {summary['missing_in']}"
        )

        hr_report.append(
            f"❌ Missing Punch Out : {summary['missing_out']}"
        )

        hr_report.append(
            f"🟢 Overtime : {summary['overtime']}"
        )

        hr_report.append("")

        hr_report.append(
            "══════════════════════════════════════"
        )

        hr_report.append("")

        # ==========================================
        # LATE REPORT HEADER
        # ==========================================

        late_report.append(
            "══════════════════════════════════════"
        )

        late_report.append(
            "🏢 ADISTHAM VENTURES PRIVATE LIMITED"
        )

        late_report.append(
            "🔴 LATE PUNCH & MISSING PUNCH OUT REPORT"
        )

        late_report.append(
            f"📅 Date : {today}"
        )

        late_report.append(
            f"🕒 Generated : {current_time}"
        )

        late_report.append("")

        late_report.append(
            f"👥 Total Employees : {summary['total']}"
        )

        late_report.append(
            f"🔴 Late Punch : {summary['late_in']}"
        )

        late_report.append(
            f"❌ Missing Punch Out : {summary['missing_out']}"
        )

        late_report.append(
            "══════════════════════════════════════"
        )

        late_report.append("")
        # ==========================================
        # LATE PUNCH IN
        # ==========================================

        GRACE_TIME = "09:11 AM"

        hr_report.append(f"🔴 LATE PUNCH IN (After {GRACE_TIME})")
        hr_report.append("")

        late_report.append(f"🔴 LATE PUNCH IN (After {GRACE_TIME})")
        late_report.append("")

        count = 1

        for emp in employees:

            late_status = next(
                (
                    s for s in emp["status"]
                    if "Late" in s
                ),
                ""
            )

            if late_status:

                employee_text = f"""
{count})

👤 Name          : {emp['name']}
🆔 Employee ID   : {emp['employee_id']}
📱 WhatsApp      : +91{emp['phone']}
📞 Phone         : {emp['phone']}
📧 Email         : {emp.get('email', '-')}
🕘 Punch In      : {emp['punch_in']}
🕕 Punch Out     : {emp['punch_out']}
⚠️ Status        : Late Punch in .

📝 Remark        : Employee Reported Late . 

🚨 Action        : Counsel Employee If Late Attendance is frequent .

────────────────────────────────────
"""

                hr_report.append(employee_text)

                late_report.append(employee_text)

                count += 1

        if count == 1:

            hr_report.append(
                "✅ No employees reported late."
            )

            late_report.append(
                "✅ No employees reported late."
            )

        hr_report.append("")

        late_report.append("")

        late_report.append(
            "══════════════════════════════════════"
        )

        late_report.append("")
        # ==========================================
        # MISSING PUNCH OUT
        # ==========================================

        hr_report.append(
            "❌ MISSING PUNCH OUT"
        )

        hr_report.append("")

        late_report.append(
            "❌ MISSING PUNCH OUT"
        )

        late_report.append("")

        count = 1

        for emp in employees:

            if "Missing Punch Out" in emp["status"]:

                employee_text = f"""
{count})

👤 Name          : {emp['name']}
🆔 Employee ID   : {emp['employee_id']}
📱 WhatsApp      : +91{emp['phone']}
📞 Phone         : {emp['phone']}
📧 Email         : {emp.get('email', '-')}

🕘 Punch In      : {emp['punch_in']}
🕕 Punch Out     : --

⚠️ Status        : Missing Punch Out .

📝 Remark        : Employee Forget to Punch Out . 

🚨 Action        : Employee Must Complete Punch Out or Contact HR .

────────────────────────────────────
"""

                hr_report.append(employee_text)

                late_report.append(employee_text)

                count += 1

        if count == 1:

            hr_report.append(
                "✅ No employees with missing punch out."
            )

            late_report.append(
                "✅ No employees with missing punch out."
            )

        hr_report.append("")

        late_report.append("")

        late_report.append(
            "══════════════════════════════════════"
        )

        late_report.append("")
        # ==========================================
        # EARLY PUNCH OUT
        # ==========================================

        hr_report.append(
            "🟠 EARLY PUNCH OUT"
        )

        hr_report.append("")

        count = 1

        for emp in employees:

            early_status = next(

                (
                    s for s in emp["status"]
                    if "Early" in s
                ),

                ""

            )

            if early_status:

                hr_report.append(f"""
{count})

👤 Name          : {emp['name']}
🆔 Employee ID   : {emp['employee_id']}
📱 WhatsApp      : +91{emp['phone']}
📞 Phone         : {emp['phone']}
📧 Email         : {emp.get('email','-')}

🕘 Punch In      : {emp['punch_in']}
🕕 Punch Out     : {emp['punch_out']}

⚠️ Status        : Early Punch Out .

📝 Remark        : Employee Left Before Shift . 

🚨 Action        : Verify Whether Prior Approval Was Obtained .

────────────────────────────────────
""")

                count += 1

        if count == 1:

            hr_report.append(
                "✅ No employees punched out early."
            )

        hr_report.append("")

        hr_report.append(
            "══════════════════════════════════════"
        )

        hr_report.append("")
        # ==========================================
        # MISSING PUNCH IN
        # ==========================================

        hr_report.append(
            "❌ MISSING PUNCH IN"
        )

        hr_report.append("")

        count = 1

        for emp in employees:

            if "Missing Punch In" in emp["status"]:

                hr_report.append(f"""
{count})

👤 Name          : {emp['name']}
🆔 Employee ID   : {emp['employee_id']}
📱 WhatsApp      : +91{emp['phone']}
📞 Phone         : {emp['phone']}
📧 Email         : {emp.get('email', '-')}

🕘 Punch In      : --
🕕 Punch Out     : {emp['punch_out']}

⚠️ Status        : Missing Punch In .

📝 Remark        : Employee Forget to Punch in . 

🚨 Action        : Employee must Contact HR to Regularize Attendance .

────────────────────────────────────
""")

                count += 1

        if count == 1:

            hr_report.append(
                "✅ No employees with missing punch in."
            )

        hr_report.append("")

        hr_report.append(
            "══════════════════════════════════════"
        )

        hr_report.append("")
        # ==========================================
        # OVERTIME
        # ==========================================

        hr_report.append(
            "🟢 OVERTIME"
        )

        hr_report.append("")

        count = 1

        for emp in employees:

            ot_status = next(

                (
                    s for s in emp["status"]
                    if "Overtime" in s
                ),

                ""

            )

            if ot_status:

                hr_report.append(f"""
{count})

👤 Name          : {emp['name']}
🆔 Employee ID   : {emp['employee_id']}
📱 WhatsApp      : +91{emp['phone']}
📞 Phone         : {emp['phone']}
📧 Email         : {emp.get('email', '-')}

🕘 Punch In      : {emp['punch_in']}
🕕 Punch Out     : {emp['punch_out']}

⚡ Status        : Overtime

📝 Remark        : Employee Worked beyond Scheduled Shift . 

🚨 Action        : Verify and Approve Overtime if Applicable .

────────────────────────────────────
""")

                count += 1

        if count == 1:

            hr_report.append(
                "✅ No overtime employees."
            )

        hr_report.append("")

        hr_report.append(
            "══════════════════════════════════════"
        )

        hr_report.append("")
        
        # ==========================================
        # ON TIME
        # ==========================================

        hr_report.append("✅ ON TIME")
        hr_report.append("")

        count = 1

        for emp in employees:

            if emp["status"] == ["On Time"]:

                hr_report.append(f"""
            {count})

👤 Name          : {emp['name']}
🆔 Employee ID   : {emp['employee_id']}
📱 WhatsApp      : +91{emp['phone']}
📞 Phone         : {emp['phone']}
📧 Email         : {emp.get('email', '-')}

🕘 Punch In      : {emp['punch_in']}
🕕 Punch Out     : {emp['punch_out']}

✅ Status        : On Time

📝 Remark        : Attendance recorded successfully.

🚨 Action        : No action required.

    ────────────────────────────────────
        """)

            count += 1

        if count == 1:

            hr_report.append("✅ No employees with On Time attendance.")

        hr_report.append("")
        hr_report.append("══════════════════════════════════════")
        # ==========================================
        # LATE REPORT SUMMARY
        # ==========================================

        late_report.append(
            "📊 SUMMARY"
        )

        late_report.append("")

        late_report.append(
            f"👥 Total Employees      : {summary['total']}"
        )

        late_report.append(
            f"🔴 Total Late Punch     : {summary['late_in']}"
        )

        late_report.append(
            f"❌ Missing Punch Out    : {summary['missing_out']}"
        )

        late_report.append("")

        late_report.append(
            "══════════════════════════════════════"
        )

        # ==========================================
        # FOOTER
        # ==========================================

        # ==========================================
        # FINAL SUMMARY
        # ==========================================

        hr_report.append("")

        hr_report.append("📊 FINAL SUMMARY")

        hr_report.append("")

        hr_report.append(
            f"👥 Total Employees : {summary['total']}"
        )

        hr_report.append(
            f"🟢 Present : {present}"
        )

        hr_report.append(
            f"🔴 Late Punch : {summary['late_in']}"
        )

        hr_report.append(
            f"🟠 Early Punch Out : {summary['early_out']}"
        )

        hr_report.append(
            f"❌ Missing Punch In : {summary['missing_in']}"
        )

        hr_report.append(
            f"❌ Missing Punch Out : {summary['missing_out']}"
        )

        hr_report.append(
            f"🟢 Overtime : {summary['overtime']}"
        )

        # ==========================================
# FOOTER
# ==========================================

        hr_report.append(
            "Generated Automatically"
        )

        hr_report.append("")

        hr_report.append(
            "Attendance Notification System Pro"
        )

        hr_report.append("")

        hr_report.append(
            "Developed by Maharajan"
        )

        hr_report.append("")

        hr_report.append(
            "🏢 ADISTHAM VENTURES PRIVATE LIMITED"
        )

        hr_report.append("")

        hr_report.append(
            "End of Report"
        )

        hr_report.append("")

        hr_report.append(
            "══════════════════════════════════════"
        )

        late_report.append(
            "Generated Automatically"
        )

        late_report.append("")

        late_report.append(
            "Attendance Notification System Pro"
        )

        late_report.append("")

        late_report.append(
            "Developed by Maharajan"
        )

        late_report.append("")

        late_report.append(
            "🏢 ADISTHAM VENTURES PRIVATE LIMITED"
        )

        late_report.append("")

        late_report.append(
            "End of Report"
        )

        late_report.append("")

        late_report.append(
            "══════════════════════════════════════"
        )
        # ==========================================
        # RETURN REPORTS
        # ==========================================

        return {

            "hr_report": "\n".join(hr_report),

            "late_punch_report": "\n".join(late_report)

        }