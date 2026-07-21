"""
=========================================================
Attendance Notification System Pro
Notification Service
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
"""


class NotificationService:
    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        pass
    # =====================================================
    # Generate Employee Notification
    # =====================================================

    def generate_message(

        self,

        employee

    ):

        message = []

        message.append(

            f"Hello {employee['name']},"

        )

        message.append("")

        message.append(

            "Attendance Notification"

        )

        message.append(

            "--------------------------------"

        )

        message.append(

            f"Employee ID : {employee['employee_id']}"

        )

        message.append(

            f"Department : {employee['department']}"

        )

        message.append("")
        # =====================================================
        # Attendance Status
        # =====================================================

        if "Missing Punch In" in employee["status"]:

            message.append(

                "❌ Missing Punch In"

            )

        if "Missing Punch Out" in employee["status"]:

            message.append(

                "❌ Missing Punch Out"

            )

        if any(

            "Late" in status

            for status in employee["status"]

        ):

            message.append(

                "⚠️ Late Punch"

            )

        if any(

            "Early" in status

            for status in employee["status"]

        ):

            message.append(

                "⚠️ Early Punch Out"

            )

        message.append("")
        # =====================================================
        # Overtime Details
        # =====================================================

        message.append(

            f"🕒 Today's OT : {employee['daily_ot']}"

        )

        message.append(

            f"📅 Monthly OT : {employee['monthly_ot']}"

        )

        message.append(

            f"⏳ Remaining OT : {employee['remaining_ot']}"

        )

        message.append("")
        # =====================================================
        # Monthly OT Status
        # =====================================================

        if employee["monthly_status"] == "Warning":

            message.append(

                "⚠️ Warning: Monthly OT has crossed 21 hours."

            )

        elif employee["monthly_status"] == "Limit Reached":

            message.append(

                "🚨 Monthly OT Limit Reached (25:00 Hours)."

            )

            message.append(

                "Further overtime requires HR approval."

            )

        elif employee["monthly_status"] == "Exceeded":

            message.append(

                "❌ Monthly OT Limit Exceeded."

            )

            message.append(

                "Please contact HR immediately."

            )

        else:

            message.append(

                "✅ Monthly OT is within the allowed limit."

            )

        message.append("")
        # =====================================================
        # Closing Message
        # =====================================================

        message.append(

            "Thank you."

        )

        message.append(

            "HR Department"

        )

        return "\n".join(message)
    # =====================================================
    # Generate All Notifications
    # =====================================================

    def generate_all(

        self,

        employees

    ):

        notifications = []

        for employee in employees:

            notifications.append({

                "employee_id": employee.get(

                    "employee_id",

                    ""

                ),

                "name": employee.get(

                    "name",

                    ""

                ),

                "phone": employee.get(

                    "phone",

                    ""

                ),

                "email": employee.get(

                    "email",

                    ""

                ),

                "message": self.generate_message(

                    employee

                )

            })

        return notifications
    # =====================================================
    # Display Notifications
    # =====================================================

    def print_notifications(

        self,

        employees

    ):

        notifications = self.generate_all(

            employees

        )

        for item in notifications:

            print("=" * 70)

            print(

                "Employee ID :",

                item["employee_id"]

            )

            print(

                "Employee    :",

                item["name"]

            )

            print(

                "Phone       :",

                item["phone"]

            )

            print(

                "Email       :",

                item["email"]

            )

            print()

            print(

                item["message"]

            )

            print()