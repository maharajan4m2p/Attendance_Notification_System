"""
=========================================
HR Report Generator
Developed by Maharajan
=========================================
"""
from datetime import datetime

class HRReportGenerator:

    def generate(self, employees, summary):

        report = []

        today = datetime.now().strftime("%d-%b-%Y")
        
        current_time = datetime.now().strftime("%I:%M %p")

        report.append("══════════════════════════════════════")
        report.append("🏢 ADISTHAM VENTURES PRIVATE LIMITED")
        report.append("📢 DAILY ATTENDANCE REPORT")
        report.append(f"📅 Date : {today}")
        report.append(f"🕒 Generated : {current_time}")
        report.append("══════════════════════════════════════")
        report.append("")

        report.append("══════════════════════════════════════")
        present = summary["total"] - summary["missing_in"]
        report.append(f"👥 Total Employees : {summary['total']}")
        report.append(f"🟢 Present : {present}")
        report.append(f"🔴 Late Punch In : {summary['late_in']}")
        report.append(f"🟠 Early Punch Out : {summary['early_out']}")
        report.append(f"❌ Missing Punch In : {summary['missing_in']}")
        report.append(f"❌ Missing Punch Out : {summary['missing_out']}")
        report.append(f"🟢 Overtime : {summary['overtime']}")
        report.append("══════════════════════════════════════")
        report.append("")

        # -------------------------
        # Late Punch
        # -------------------------

        report.append("🔴 LATE PUNCH IN")
        

        count = 1

        for emp in employees:

            late_status = next(
                (s for s in emp["status"] if "Late" in s),
                ""
            )

            if late_status:

                report.append(
        f"""
        {count})

        👤 Name      : {emp['name']}

        🆔 Emp ID    : {emp['employee_id']}

        🕘 Punch In  : {emp['punch_in']}

        ⚠️ Status    : {late_status}

        ────────────────────────
        """
            )

            count += 1
        report.append("--------------------------------")

        # -------------------------
        # Early Punch Out
        # -------------------------

        report.append("🔴 LATE PUNCH IN")

        count = 1

        for emp in employees:

            late_status = next(
                (s for s in emp["status"] if "Late" in s),
                ""
            )

            if late_status:

                report.append(
        f"""
        {count})

👤 Name      : {emp['name']}
🆔 Emp ID    : {emp['employee_id']}
🕘 Punch In  : {emp['punch_in']}
⚠️ Status    : {late_status}

────────────────────────
"""
                )

                count += 1

        report.append("--------------------------------")

        # -------------------------
        # Missing Punch Out
        # -------------------------

        report.append("❌ MISSING PUNCH OUT")

        for emp in employees:

            if "Missing Punch Out" in emp["status"]:

                report.append(
                    f"""
        👤 {emp['name']}
        🆔 {emp['employee_id']}
        🕘 Punch In : {emp['punch_in']}
"""
                )

        report.append("--------------------------------")

        # -------------------------
        # Missing Punch In
        # -------------------------

        report.append("❌ MISSING PUNCH IN")

        for emp in employees:

            if "Missing Punch In" in emp["status"]:

                report.append(
                    f"""
        👤 {emp['name']}
        🆔 {emp['employee_id']}
        🕕 Punch Out : {emp['punch_out']}
"""
                )

        report.append("--------------------------------")

        # -------------------------
        # Overtime
        # -------------------------

        report.append("🟢 OVERTIME")

        count = 1

        for emp in employees:

            ot_status = next(
                (s for s in emp["status"] if "Overtime" in s),
                ""
            )

            if ot_status:

                report.append(
        f"""
        {count})

👤 Name      : {emp['name']}
🆔 Emp ID    : {emp['employee_id']}
🕕 Punch Out : {emp['punch_out']}
⚡ Status    : {ot_status}

────────────────────────
"""
        )

        count += 1

        report.append("")
        report.append("══════════════════════════════════════")
        report.append("Generated Automatically")
        report.append("Attendance Notification System Pro")
        report.append("Developed by Maharajan")
        report.append("══════════════════════════════════════")

        return "\n".join(report)