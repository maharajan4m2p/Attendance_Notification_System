"""
=========================================================
Attendance Notification System Pro
Attendance Checker
Version : 2.0
Developed by Maharajan
=========================================================
"""

from datetime import datetime
import pandas as pd

from config import (

    SHIFT_IN,

    SHIFT_OUT,

    GRACE_TIME,

    EARLY_OUT_TIME,

    OVERTIME_AFTER,

    STATUS_PRESENT,

    STATUS_LATE,

    STATUS_EARLY,

    STATUS_MISSING_IN,

    STATUS_MISSING_OUT,

    STATUS_OVERTIME

)


class AttendanceChecker:

    # =====================================================
    # Initialize Shift Timings
    # =====================================================

    def __init__(self):

        self.shift_in = datetime.strptime(

            SHIFT_IN,

            "%H:%M"

        )

        self.shift_out = datetime.strptime(

            SHIFT_OUT,

            "%H:%M"

        )

        self.grace_time = datetime.strptime(

            GRACE_TIME,

            "%H:%M"

        )

        self.early_out_time = datetime.strptime(

            EARLY_OUT_TIME,

            "%H:%M"

        )

        self.overtime_after = datetime.strptime(

            OVERTIME_AFTER,

            "%H:%M"

        )
        # =====================================================
    # Convert Excel Time to datetime
    # =====================================================

    def convert_time(self, value):

        if pd.isna(value):
            return None

    # Already datetime
        if isinstance(value, datetime):
            return value

    # Integer (9 -> 09:00)
        if isinstance(value, int):
            return datetime.strptime(f"{value:02d}:00", "%H:%M")

    # Float (8.55, 9.3, 4.3)
        if isinstance(value, float):

            hours = int(value)

            decimal = round(value - hours, 2)

            if decimal == 0:
                minutes = 0
            else:
                minutes = int(decimal * 100)

            # Convert .3 -> 30 minutes
                if minutes < 10:
                    minutes *= 10

            if minutes >= 60:
                return None

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

            "%I:%M%p"

        ]

        for fmt in formats:

            try:
                return datetime.strptime(value, fmt)
            except:
                pass

        return None


    # =====================================================
    # Calculate Minutes Between Times
    # =====================================================

    def minutes_between(

        self,

        start,

        end

    ):

        if start is None or end is None:

            return 0

        return int(

            (end - start).total_seconds() / 60

        )


    # =====================================================
    # Format Time
    # =====================================================

    def format_time(self, value):

        if value is None:

            return "--"

        return value.strftime(

            "%I:%M %p"

        )


    # =====================================================
    # Format Duration
    # =====================================================

    def format_duration(

        self,

        minutes

    ):

        if minutes <= 0:

            return "0 minute(s)"
        
        hours = minutes // 60

        mins = minutes % 60

        if hours == 0:

            return f"{mins} minute(s)"

        return f"{hours} hour(s) {mins} minute(s)"
    # =====================================================
    # Process Attendance Excel
    # =====================================================

    def process_excel(

        self,

        excel_file

    ):

        dataframe = pd.read_excel(

            excel_file

        )

        # Remove completely empty rows

        dataframe = dataframe.dropna(

            how="all"

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

        # ==========================================
        # Process Each Employee
        # ==========================================

        for _, row in dataframe.iterrows():

            employee = {}

            employee["employee_id"] = str(

                row.get("Employee ID",row.get("Employee", ""))

            ).strip()

            employee["name"] = str(

                row.get("Name", "")

            ).strip()

            employee["phone"] = str(

                row.get("Phone", "")

            ).strip()

            employee["email"] = str(

                row.get("Email", row.get("email",""))

            ).strip()

            raw_in = row.get(

                "Punch In",

                ""

            )

            raw_out = row.get(

                "Punch Out",

                ""

            )

            in_time = self.convert_time(

                raw_in

            )

            out_time = self.convert_time(

                raw_out

            )

            # ==========================================
            # Convert Afternoon Punch Out
            # ==========================================

            if out_time is not None:

                if out_time.hour <= 9:

                    out_time = out_time.replace(hour=out_time.hour +12)

            employee["punch_in"] = self.format_time(

                in_time

            )

            employee["punch_out"] = self.format_time(

                out_time

            )

            employee["status"] = []

            employee["notification"] = ""

            employee["late_minutes"] = 0

            employee["early_minutes"] = 0

            employee["overtime_minutes"] = 0
            # =====================================
            # Punch In Validation
            # =====================================

            if in_time is None:

                employee["status"].append(
                    STATUS_MISSING_IN
                )

                summary["missing_in"] += 1

            elif in_time > self.grace_time:

                late = self.minutes_between(

                    self.shift_in,

                    in_time

                )

                employee["late_minutes"] = late

                employee["status"].append(

                    f"{STATUS_LATE} ({late} min)"

                )

                summary["late_in"] += 1

            else:

                employee["status"].append(

                    STATUS_PRESENT

                )


            # =====================================
            # Punch Out Validation
            # =====================================

            if out_time is None:

                employee["status"].append(

                    STATUS_MISSING_OUT

                )

                summary["missing_out"] += 1

            else:

                # Early Punch Out

                if out_time < self.early_out_time:

                    early = self.minutes_between(

                        out_time,

                        self.shift_out

                    )

                    employee["early_minutes"] = early

                    employee["status"].append(

                        f"{STATUS_EARLY} ({early} min)"

                    )

                    summary["early_out"] += 1

                # Overtime

                elif out_time > self.overtime_after:

                    overtime = self.minutes_between(

                        self.shift_out,

                        out_time

                    )

                    employee["overtime_minutes"] = overtime

                    employee["status"].append(

                        f"{STATUS_OVERTIME} ({overtime} min)"

                    )

                    summary["overtime"] += 1


            # =====================================
            # Attendance Remark
            # =====================================

            if len(employee["status"]) == 1 and employee["status"][0] == STATUS_PRESENT:

                employee["remark"] = "Perfect Attendance"

            elif STATUS_MISSING_IN in employee["status"]:

                employee["remark"] = "Missing Punch In"

            elif STATUS_MISSING_OUT in employee["status"]:

                employee["remark"] = "Missing Punch Out"

            elif any(STATUS_LATE in s for s in employee["status"]):

                employee["remark"] = "Late Arrival"

            elif any(STATUS_EARLY in s for s in employee["status"]):

                employee["remark"] = "Left Early"

            elif any(STATUS_OVERTIME in s for s in employee["status"]):

                employee["remark"] = "Worked Overtime"

            else:

                employee["remark"] = "Attendance Recorded"
                # =====================================
            # Build Notification Message
            # =====================================

            messages = []

            if STATUS_MISSING_IN in employee["status"]:

                messages.append(
                    "❌ Your Punch In is missing."
                )

                messages.append(
                    "Please contact HR if this is incorrect."
                )

            if STATUS_MISSING_OUT in employee["status"]:

                messages.append(
                    "❌ Your Punch Out is missing."
                )

                messages.append(
                    "Please complete your Punch Out."
                )

            if employee["late_minutes"] > 0:

                messages.append(
                    f"🕘 Punch In : {employee['punch_in']}"
                )

                messages.append(
                    f"⚠️ You reported {self.format_duration(employee['late_minutes'])} late."
                )

            if employee["early_minutes"] > 0:

                messages.append(
                    f"🕕 Punch Out : {employee['punch_out']}"
                )

                messages.append(
                    f"⚠️ You left early by {self.format_duration(employee['early_minutes'])}."
                )

                messages.append(
                    f"Scheduled Shift End : {self.shift_out.strftime('%I:%M %p')}"
                )

            if employee["overtime_minutes"] > 0:

                messages.append(
                    f"🕕 Punch Out : {employee['punch_out']}"
                )

                messages.append(
                    f"✅ Overtime Worked : {self.format_duration(employee['overtime_minutes'])}"
                )

            # =====================================
            # Final Notification
            # =====================================

            if len(messages) == 0:

                employee["notification"] = (
                    f"Hello {employee['name']},\n\n"
                    "✅ Your attendance has been recorded successfully.\n\n"
                    f"Employee ID : {employee['employee_id']}\n"
                    f"Punch In : {employee['punch_in']}\n"
                    f"Punch Out : {employee['punch_out']}\n"
                    f"Status : {', '.join(employee['status'])}\n\n"
                    "Thank you.\n"
                    "HR Department\n"
                    "ADISTHAM VENTURES PRIVATE LIMITED"
                )

            else:

                employee["notification"] = (
                    f"Hello {employee['name']},\n\n"
                    "Attendance Notification\n\n"
                    + "\n".join(messages)
                    + "\n\nEmployee ID : "
                    + employee["employee_id"]
                    + "\nStatus : "
                    + ", ".join(employee["status"])
                    + "\n\nThank you.\n"
                    "HR Department\n"
                    "ADISTHAM VENTURES PRIVATE LIMITED"
                )

            employees.append(employee)

        # =====================================
        # Sort Employees by Employee ID
        # =====================================

        employees = sorted(

            employees,

            key=lambda x: x["employee_id"]

        )

        # =====================================
        # Return Result
        # =====================================

        return {

            "summary": summary,

            "employees": employees

        }