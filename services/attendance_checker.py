"""
=========================================================
Attendance Notification System
Attendance Checker Pro
Developed by Maharajan
=========================================================
"""

from datetime import datetime
import pandas as pd

from config import SHIFT_IN, SHIFT_OUT


class AttendanceChecker:

    def __init__(self):

        self.shift_in = datetime.strptime(
            SHIFT_IN,
            "%H:%M"
        )

        self.shift_out = datetime.strptime(
            SHIFT_OUT,
            "%H:%M"
        )

    # =====================================================
    # Convert Any Excel Time
    # =====================================================

    def convert_time(self, value):

        if pd.isna(value):
            return None

        try:

            # Excel datetime
            if isinstance(value, datetime):
                return value

            # Excel float
            if isinstance(value, (int, float)):

                hours = int(value)
                minutes = round((value - hours) * 100)

                return datetime.strptime(
                    f"{hours:02d}:{minutes:02d}",
                    "%H:%M"
                )

            value = str(value).strip()

            if value == "":
                return None

            value = value.replace(".", ":")

            formats = [

                "%H:%M",

                "%H:%M:%S",

                "%I:%M %p",

                "%I:%M%p",

                "%I.%M %p",

                "%I.%M%p"

            ]

            for fmt in formats:

                try:

                    return datetime.strptime(
                        value,
                        fmt
                    )

                except:
                    pass

            return None

        except:

            return None

    # =====================================================
    # Minutes Difference
    # =====================================================

    def minutes_between(
        self,
        start,
        end
    ):

        return int(
            (end - start).total_seconds() / 60
        )

    # =====================================================
    # Format Time
    # =====================================================

    def format_time(self, value):

        if value is None:
            return "--"

        return value.strftime("%I:%M %p")

    # =====================================================
    # Format Duration
    # =====================================================

    def format_duration(
        self,
        minutes
    ):

        hours = minutes // 60

        mins = minutes % 60

        if hours == 0:

            return f"{mins} minute(s)"

        return f"{hours} hour(s) {mins} minute(s)"

    # =====================================================
    # Process Excel
    # =====================================================

    def process_excel(
        self,
        excel_file
    ):

        dataframe = pd.read_excel(
            excel_file
        )

        employees = []

        summary = {

            "total": len(dataframe),

            "late_in": 0,

            "missing_in": 0,

            "missing_out": 0,

            "early_out": 0,

            "overtime": 0

        }
        # ============================================
        # Process Every Employee
        # ============================================

        for _, row in dataframe.iterrows():

            employee = {}

            employee["employee_id"] = str(
                row.get("Employee ID", "")
            )

            employee["name"] = str(
                row.get("Name", "")
            ).strip()

            employee["phone"] = str(
                row.get("Phone", "")
            ).strip()

            raw_in = row.get("Punch In", "")

            raw_out = row.get("Punch Out", "")

            in_time = self.convert_time(raw_in)

            out_time = self.convert_time(raw_out)
            # ===========================================
            # Fix AM / PM
            # ===========================================

            # Punch In (06:00 AM - 11:59 AM)
            if in_time is not None:

                if 1 <= in_time.hour <= 8:
                # Keep as morning (08:55 stays 08:55 AM)
                    pass

                # Punch Out (01:00 PM - 08:59 PM)
            if out_time is not None:

            # Convert 4.30 -> 16.30
                if 1 <= out_time.hour <= 8:
                    out_time = out_time.replace(hour=out_time.hour + 12)

            # Keep 17:50, 18:30 etc. unchanged

            employee["punch_in"] = self.format_time(in_time)

            employee["punch_out"] = self.format_time(out_time)

            employee["status"] = []

            employee["notification"] = ""

            # =====================================
            # Missing Punch In
            # =====================================

            if in_time is None:

                employee["status"].append(
                    "Missing Punch In"
                )

                summary["missing_in"] += 1

            # =====================================
            # Late Punch In
            # =====================================

            elif in_time > self.shift_in:

                late = self.minutes_between(
                    self.shift_in,
                    in_time
                )

                employee["late_minutes"] = late

                employee["status"].append(
                    f"Late Punch In ({late} min)"
                )

                summary["late_in"] += 1

            else:

                employee["status"].append(
                    "On Time"
                )

            # =====================================
            # Missing Punch Out
            # =====================================

            if out_time is None:

                employee["status"].append(
                    "Missing Punch Out"
                )

                summary["missing_out"] += 1

            # =====================================
            # Early Punch Out
            # =====================================

            elif out_time < self.shift_out:

                early = self.minutes_between(
                    out_time,
                    self.shift_out
                )

                employee["early_minutes"] = early

                employee["status"].append(
                    f"Early Punch Out ({early} min)"
                )

                summary["early_out"] += 1

            # =====================================
            # Overtime
            # =====================================

            elif out_time > self.shift_out:

                overtime = self.minutes_between(
                    self.shift_out,
                    out_time
                )

                employee["overtime_minutes"] = overtime

                employee["status"].append(
                    f"Overtime ({overtime} min)"
                )

                summary["overtime"] += 1
                # =====================================
            # Build Notification Message
            # =====================================

            messages = []

            if "Missing Punch In" in employee["status"]:

                messages.append(
                    "❌ Your Punch In is missing."
                )

                messages.append(
                    "Please contact HR if this is incorrect."
                )

            if "Missing Punch Out" in employee["status"]:

                messages.append(
                    "❌ Your Punch Out is missing."
                )

                messages.append(
                    "Please complete your Punch Out."
                )

            if "late_minutes" in employee:

                messages.append(
                    f"🕘 Punch In : {employee['punch_in']}"
                )

                messages.append(
                    f"⚠️ You reported {self.format_duration(employee['late_minutes'])} late."
                )

            if "early_minutes" in employee:

                messages.append(
                    f"🕕 Punch Out : {employee['punch_out']}"
                )

                messages.append(
                    "⚠️ You punched out early."
                )

                messages.append(
                    f"Early By : {self.format_duration(employee['early_minutes'])}"
                )

                messages.append(
                    "Scheduled Shift End : 06:00 PM"
                )

            if "overtime_minutes" in employee:

                messages.append(
                    f"🕕 Punch Out : {employee['punch_out']}"
                )

                messages.append(
                    f"✅ Overtime : {self.format_duration(employee['overtime_minutes'])}"
                )

            # =====================================
            # Final Notification
            # =====================================

            if len(messages) == 0:

                employee["notification"] = (
                    f"Hello {employee['name']},\n\n"
                    "✅ Attendance recorded successfully.\n\n"
                    f"Punch In : {employee['punch_in']}\n"
                    f"Punch Out : {employee['punch_out']}\n\n"
                    "Thank you,\nHR Department"
                )

            else:

                employee["notification"] = (
                    f"Hello {employee['name']},\n\n"
                    "Attendance Notification\n\n"
                    + "\n".join(messages)
                    + "\n\nThank you,\nHR Department"
                )

            employees.append(employee)

        # =====================================
        # Return Result
        # =====================================

        return {

            "summary": summary,

            "employees": employees

        }