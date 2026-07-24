"""
=========================================================
Attendance Notification System Pro
Notification Service
Version : 10.0 Enterprise
=========================================================
"""


class NotificationService:
    """
    Enterprise Notification Service

    Features
    --------
    • Employee Attendance Notification
    • Daily OT Notification
    • Monthly OT Notification
    • Professional Message Format
    • HR Friendly
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.footer = [

            "",

            "Regards,",

            "HR Department",

            "Attendance Notification System Pro"

        ]
        # =====================================================
    # Generate Employee Notification
    # =====================================================

    def generate_message(
        self,
        employee
    ):

        message = []

        # =====================================================
        # Employee Information
        # =====================================================

        message.extend([

            "📢 Attendance Notification",

            "",

            f"👤 Employee : {employee.get('name', '')}",

            f"🆔 Employee ID : {employee.get('employee_id', '')}",

            f"🏢 Department : {employee.get('department', '')}",

            f"💼 Designation : {employee.get('designation', '')}",

            "",

            f"📅 Attendance Date : {employee.get('attendance_date', '')}",

            f"🕘 Punch In : {employee.get('punch_in', '--')}",

            f"🕔 Punch Out : {employee.get('punch_out', '--')}",

            ""

        ])

        # =====================================================
        # Attendance Status
        # =====================================================

        status_list = employee.get(
            "status",
            []
        )

        message.append(
            "📋 Attendance Status"
        )

        if status_list:

            for status in status_list:

                message.append(
                    f"• {status}"
                )

        else:

            message.append(
                "✅ On Time"
            )

        message.append("")

        # =====================================================
        # Daily & Monthly Status
        # =====================================================

        message.extend([

            f"📌 Daily Status : {employee.get('daily_status', 'Normal')}",

            f"📊 Monthly Status : {employee.get('monthly_status', 'Normal')}",

            ""

        ])

        # =====================================================
        # Overtime Details
        # =====================================================

        message.extend([

            f"🕒 Daily OT : {employee.get('daily_ot', '00:00')}",

            f"📅 Monthly OT : {employee.get('monthly_ot', '00:00')}",

            f"⏳ Remaining OT : {employee.get('remaining_ot', '00:00')}",

            ""

        ])

        # =====================================================
        # Monthly OT Message
        # =====================================================

        monthly_status = employee.get(
            "monthly_status",
            "Normal"
        )

        message.extend(

            self.get_monthly_status_message(
                monthly_status
            )

        )

        message.append("")

        # =====================================================
        # Footer
        # =====================================================

        message.extend(
            self.footer
        )

        return "\n".join(
            message
        )
        # =====================================================
    # Check Employee Status
    # =====================================================

    def has_status(
        self,
        employee,
        keyword
    ):

        status_list = employee.get(
            "status",
            []
        )

        if not status_list:

            return False

        keyword = str(
            keyword
        ).strip().lower()

        return any(

            keyword in str(status).strip().lower()

            for status in status_list

        )
        # =====================================================
    # Get Monthly Status Message
    # =====================================================

    def get_monthly_status_message(
        self,
        monthly_status
    ):

        monthly_status = str(
            monthly_status
        ).strip()

        messages = {

            "Normal": [

                "✅ Monthly overtime is within the permitted company limit."

            ],

            "Warning": [

                "⚠️ Monthly overtime has crossed the warning limit.",

                "Please monitor your overtime hours carefully."

            ],

            "Limit Reached": [

                "🚨 Monthly overtime limit has been reached.",

                "Further overtime requires HR approval."

            ],

            "Exceeded": [

                "❌ Monthly overtime limit has been exceeded.",

                "Please contact the HR Department immediately."

            ]

        }

        return messages.get(

            monthly_status,

            [

                "ℹ️ Monthly overtime status is unavailable."

            ]

        )