"""
=========================================================
Attendance Notification System Pro
Configuration File
Version : 2.0
Developed by Maharajan
=========================================================
"""

import os

# =====================================================
# Application
# =====================================================

APP_NAME = "Attendance Notification System Pro"

SECRET_KEY = "attendance_notification_secret_key"

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

# =====================================================
# Folder Paths
# =====================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)

# =====================================================
# Allowed Upload Extensions
# =====================================================

ALLOWED_EXTENSIONS = {

    "xlsx",

    "xls"

}
# =====================================================
# Company Shift Timings
# =====================================================

SHIFT_IN = "09:00"

SHIFT_OUT = "18:00"

# Grace Time
# Employees punching after this time
# are considered Late.

GRACE_TIME = "09:11"

# Early Punch Out Threshold

EARLY_OUT_TIME = "18:00"

# Overtime starts after this time

OVERTIME_AFTER = "18:00"


# =====================================================
# Attendance Rules
# =====================================================

ALLOW_EARLY_IN = True

CALCULATE_OVERTIME = True

CHECK_MISSING_IN = True

CHECK_MISSING_OUT = True

CHECK_EARLY_OUT = True

CHECK_LATE_IN = True

# =====================================================
# Attendance Status Labels
# =====================================================

STATUS_PRESENT = "Present"

STATUS_LATE = "Late Punch In"

STATUS_EARLY = "Early Punch Out"

STATUS_MISSING_IN = "Missing Punch In"

STATUS_MISSING_OUT = "Missing Punch Out"

STATUS_OVERTIME = "Overtime"
# =====================================================
# Notification Settings
# =====================================================

ENABLE_EMAIL = True

ENABLE_SMS = False

ENABLE_WHATSAPP = True

ENABLE_TEAMS = False


# =====================================================
# Report Settings
# =====================================================

GENERATE_EXCEL_REPORT = True

GENERATE_SUMMARY = True

GENERATE_HR_REPORT = True

GENERATE_LATE_PUNCH_REPORT = True

AUTO_SEND_EMAIL = True

AUTO_OPEN_WHATSAPP = False


# =====================================================
# Dashboard Settings
# =====================================================

SHOW_EMPLOYEE_EMAIL = True

SHOW_EMPLOYEE_PHONE = True

SHOW_NOTIFICATION_PREVIEW = True

SHOW_SUMMARY_CARDS = True


# =====================================================
# Automatic Folder Creation
# =====================================================

os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)

os.makedirs(

    REPORT_FOLDER,

    exist_ok=True

)
# =====================================================
# Email Configuration
# =====================================================

EMAIL_ENABLED = True

SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587

EMAIL_ADDRESS = "adishtam.hr@gmail.com"

# Gmail App Password
# Recommended:
# Store this in an environment variable for production.

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD",
    "abcd efgh ijkl mnop"
)

SMTP_TIMEOUT = 30


# =====================================================
# Company Information
# =====================================================

COMPANY_NAME = "ADISTHAM VENTURES PRIVATE LIMITED"

COMPANY_SHORT_NAME = "ADISTHAM"

HR_NAME = "HR Department"

COMPANY_EMAIL = EMAIL_ADDRESS

COMPANY_WEBSITE = ""

COMPANY_PHONE = ""


# =====================================================
# Application Information
# =====================================================

APP_VERSION = "2.0"

DEVELOPER = "Maharajan"

COPYRIGHT = "© ADISTHAM VENTURES PRIVATE LIMITED"