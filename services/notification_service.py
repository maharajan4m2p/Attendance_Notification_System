"""
=========================================================
Attendance Notification System
Notification Service
Version : 1.0
=========================================================
"""


class NotificationService:

    def __init__(self):

        pass

    # =====================================================
    # Generate Notification
    # =====================================================

    def generate_message(self, employee):

        message = []

        message.append(
            f"Hello {employee['name']},"
        )

        message.append("")

        message.append(
            "Attendance Notification"
        )

        message.append("---------------------------")

        # Late Punch In

        if "late_minutes" in employee:

            message.append(
                f"Late Punch In : {employee['late_minutes']} minute(s)"
            )

        # Missing Punch In

        if "Missing Punch In" in employee["status"]:

            message.append(
                "Missing Punch In"
            )

        # Missing Punch Out

        if "Missing Punch Out" in employee["status"]:

            message.append(
                "Missing Punch Out"
            )

        # Early Punch Out

        if "early_minutes" in employee:

            message.append(
                f"Early Punch Out : {employee['early_minutes']} minute(s)"
            )

        # Overtime

        if "overtime_minutes" in employee:

            message.append(
                f"Overtime : {employee['overtime_minutes']} minute(s)"
            )

        message.append("")
        message.append("Thank You")
        message.append("HR Department")

        return "\n".join(message)

    # =====================================================
    # Generate All Messages
    # =====================================================

    def generate_all(self, employees):

        notifications = []

        for employee in employees:

            notifications.append({

                "name": employee["name"],

                "phone": employee["phone"],

                "message": self.generate_message(employee)

            })

        return notifications

    # =====================================================
    # Display Notifications
    # =====================================================

    def print_notifications(self, employees):

        notifications = self.generate_all(
            employees
        )

        for item in notifications:

            print("=" * 60)

            print("Employee :", item["name"])

            print("Phone    :", item["phone"])

            print()

            print(item["message"])

            print()
            