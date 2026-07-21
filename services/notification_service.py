"""
=========================================================
Attendance Notification System Pro
Notification Service
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""


class NotificationService:
    """
    Enterprise Notification Service

    Features
    --------
    • Employee Attendance Notification
    • Monthly OT Notification
    • Professional Message Format
    • High Performance
    """

    # =====================================================
    # Initialize
    # =====================================================

    def __init__(self):

        self.footer = [

            "",

            "Regards,",

            "HR Department"

        ]

    # =====================================================
    # Generate Employee Notification
    # =====================================================

    def generate_message(

        self,

        employee

    ):

        message = []

        message.extend([

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

        if status_list:

            message.append(

                "Attendance Status"

            )

            for status in status_list:

                message.append(

                    f"• {status}"

                )

        else:

            message.append(

                "• On Time"

            )

        message.append("")

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
        # Monthly OT Status
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

        return any(

            keyword.lower() in str(status).lower()

            for status in status_list

        )

    # =====================================================
    # Get Monthly Status Message
    # =====================================================

    def get_monthly_status_message(

        self,

        monthly_status

    ):

        if monthly_status == "Warning":

            return [

                "⚠️ Monthly overtime has crossed the warning limit."

            ]

        elif monthly_status == "Limit Reached":

            return [

                "🚨 Monthly overtime limit reached.",

                "Further overtime requires HR approval."

            ]

        elif monthly_status == "Exceeded":

            return [

                "❌ Monthly overtime limit exceeded.",

                "Please contact the HR Department."

            ]

        return [

            "✅ Monthly overtime is within the permitted limit."

        ]