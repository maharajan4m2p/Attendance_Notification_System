"""
=========================================
HR Report Generator
Developed by Maharajan
=========================================
"""

from datetime import datetime


class HRReportGenerator:

    # =====================================================
    # Generate WhatsApp HR Report
    # =====================================================

    def generate(self, employees, summary):

        report = []

        today = datetime.now().strftime("%d-%b-%Y")

        current_time = datetime.now().strftime("%I:%M %p")

        present = (
            summary["total"]
            - summary["missing_in"]
        )

        # ==========================================
        # Header
        # ==========================================

        report.append(
            "══════════════════════════════════════"
        )

        report.append(
            "🏢 ADISTHAM VENTURES PRIVATE LIMITED"
        )

        report.append(
            "📢 DAILY ATTENDANCE REPORT"
        )

        report.append(
            f"📅 Date : {today}"
        )

        report.append(
            f"🕒 Generated : {current_time}"
        )

        report.append(
            "══════════════════════════════════════"
        )

        report.append("")

        # ==========================================
        # Summary
        # ==========================================

        report.append(
            "══════════════════════════════════════"
        )

        report.append(
            f"👥 Total Employees : {summary['total']}"
        )

        report.append(
            f"🟢 Present : {present}"
        )

        report.append(
            f"🔴 Late Punch In : {summary['late_in']}"
        )

        report.append(
            f"🟠 Early Punch Out : {summary['early_out']}"
        )

        report.append(
            f"❌ Missing Punch In : {summary['missing_in']}"
        )

        report.append(
            f"❌ Missing Punch Out : {summary['missing_out']}"
        )

        report.append(
            f"🟢 Overtime : {summary['overtime']}"
        )

        report.append(
            "══════════════════════════════════════"
        )

        report.append("")
        # ==========================================
        # Late Punch In
        # ==========================================

        report.append(
            "🔴 LATE PUNCH IN (AFTER {GRACE_TIME} AM)"
        )

        report.append("")

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

                report.append(

                    f"""
{count})

👤 Name      : {emp['name']}

🆔 Employee ID : {emp['employee_id']}

👤 Mention      : @{emp['phone']}

📞 Phone     : {emp['phone']}

🕘 Punch In  : {emp['punch_in']}

⚠️ Status    : {late_status}

────────────────────────────────────
"""

                )

                count += 1

        if count == 1:

            report.append(

                "✅ No employees reported late."

            )

        report.append("")

        report.append(

            "══════════════════════════════════════"

        )

        report.append("")
        # ==========================================
        # Early Punch Out
        # ==========================================

        report.append(
            "🟠 EARLY PUNCH OUT"
        )

        report.append("")

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

                report.append(

                    f"""
{count})

👤 Name         : {emp['name']}

🆔 Employee ID  : {emp['employee_id']}

👤 Mention      : @{emp['phone']}

📞 Phone        : {emp['phone']}

🕕 Punch Out    : {emp['punch_out']}

⚠️ Status       : {early_status}

────────────────────────────────────
"""

                )

                count += 1

        if count == 1:

            report.append(

                "✅ No employees punched out early."

            )

        report.append("")

        report.append(

            "══════════════════════════════════════"

        )

        report.append("")
        # ==========================================
        # Missing Punch Out
        # ==========================================

        report.append(
            "❌ MISSING PUNCH OUT"
        )

        report.append("")

        count = 1

        for emp in employees:

            if "Missing Punch Out" in emp["status"]:

                report.append(

                    f"""
{count})

👤 Name         : {emp['name']}

🆔 Employee ID  : {emp['employee_id']}

👤 Mention      : @{emp['phone']}

📞 Phone        : {emp['phone']}

🕘 Punch In     : {emp['punch_in']}

🕕 Punch Out    : --

⚠️ Status       : Missing Punch Out

────────────────────────────────────
"""

                )

                count += 1

        if count == 1:

            report.append(

                "✅ No employees with missing punch out."

            )

        report.append("")

        report.append(

            "══════════════════════════════════════"

        )

        report.append("")
        # ==========================================
        # Missing Punch In
        # ==========================================

        report.append(
            "❌ MISSING PUNCH IN"
        )

        report.append("")

        count = 1

        for emp in employees:

            if "Missing Punch In" in emp["status"]:

                report.append(

                    f"""
{count})

👤 Name         : {emp['name']}

🆔 Employee ID  : {emp['employee_id']}

👤 Mention      : @{emp['phone']}

📞 Phone        : {emp['phone']}

🕘 Punch In     : --

🕕 Punch Out    : {emp['punch_out']}

⚠️ Status       : Missing Punch In

────────────────────────────────────
"""

                )

                count += 1

        if count == 1:

            report.append(
                "✅ No employees with missing punch in."
            )

        report.append("")

        report.append(
            "══════════════════════════════════════"
        )

        report.append("")
        # ==========================================
        # Overtime
        # ==========================================

        report.append(
            "🟢 OVERTIME"
        )

        report.append("")

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

                report.append(

                    f"""
{count})

👤 Name         : {emp['name']}

🆔 Employee ID  : {emp['employee_id']}

👤 Mention      : @{emp['phone']}

📞 Phone        : {emp['phone']}

🕕 Punch Out    : {emp['punch_out']}

⚡ Status        : {ot_status}

────────────────────────────────────
"""

                )

                count += 1

        if count == 1:

            report.append(
                "✅ No overtime employees."
            )

        report.append("")

        report.append(
            "══════════════════════════════════════"
        )

        # ==========================================
        # Footer
        # ==========================================

        report.append("")
        report.append("Generated Automatically")
        report.append("Attendance Notification System Pro")
        report.append("Developed by Maharajan")
        report.append("🏢 ADISTHAM VENTURES PRIVATE LIMITED")
        report.append("")
        report.append(
            "══════════════════════════════════════"
        )

        return "\n".join(report)