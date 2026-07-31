"""
=========================================================
Attendance Notification System Pro
Enterprise Configuration
Version : 14.0 Enterprise
=========================================================
"""

import os

# =====================================================
# Application Information
# =====================================================

APP_NAME = "Attendance Notification System Pro"

VERSION = "13.0 Enterprise"

COMPANY_NAME = "ADISTHAM VENTURES PRIVATE LIMITED"

SECRET_KEY = "attendance_notification_system"

DEBUG = True

HOST = "0.0.0.0"

PORT = 5000

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# =====================================================
# Folder Configuration
# =====================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)

DATABASE_FOLDER = os.path.join(
    BASE_DIR,
    "database"
)

LOG_FOLDER = os.path.join(
    BASE_DIR,
    "logs"
)

BACKUP_FOLDER = os.path.join(
    DATABASE_FOLDER,
    "backup"
)

# =====================================================
# Create Required Folders
# =====================================================

for folder in (
    UPLOAD_FOLDER,
    REPORT_FOLDER,
    DATABASE_FOLDER,
    LOG_FOLDER,
    BACKUP_FOLDER
):
    os.makedirs(
        folder,
        exist_ok=True
    )

# =====================================================
# Database Files
# =====================================================

MONTHLY_OT_DATABASE = os.path.join(
    DATABASE_FOLDER,
    "monthly_ot.xlsx"
)

EMPLOYEE_DATABASE = os.path.join(
    DATABASE_FOLDER,
    "employee_database.xlsx"
)

DAILY_HISTORY_DATABASE = os.path.join(
    DATABASE_FOLDER,
    "daily_history.xlsx"
)

MONTHLY_HISTORY_DATABASE = os.path.join(
    DATABASE_FOLDER,
    "monthly_history.xlsx"
)

BACKUP_DATABASE = os.path.join(
    BACKUP_FOLDER,
    "monthly_ot_backup.xlsx"
)
MONTHLY_DATABASE_REPORT = os.path.join(
    REPORT_FOLDER,
    "Monthly_Database.xlsx"
)

MONTHLY_OT_REPORT = os.path.join(
    REPORT_FOLDER,
    "Monthly_OT_Report.xlsx"
)

ATTENDANCE_REPORT = os.path.join(
    REPORT_FOLDER,
    "Attendance_Report.xlsx"
)


ATTENDANCE_REPORT_NAME = "Attendance_Report.xlsx"

MONTHLY_REPORT_NAME = "Monthly_OT_Report.xlsx"

MONTHLY_DATABASE_NAME = "Monthly_Database.xlsx"

# =====================================================
# Upload Configuration
# =====================================================

ALLOWED_EXTENSIONS = {

    "xlsx",

    "xls",

    "csv"

}

MAX_CONTENT_LENGTH = 100 * 1024 * 1024

SUPPORTED_ENCODINGS = [

    "utf-8",

    "utf-8-sig",

    "latin1",

    "cp1252",
    
    "ISO-8859-1"

]

# =====================================================
# Shift Configuration
# =====================================================

SHIFT_START = "08:30"

SHIFT_END = "17:30"

GRACE_TIME = "08:41"

LUNCH_START = "13:00"

LUNCH_END = "13:30"

STANDARD_WORKING_HOURS = 8

STANDARD_WORKING_MINUTES = 480

WORKING_DAYS_PER_MONTH = 31

# =====================================================
# Monthly OT Configuration
# =====================================================

MONTHLY_OT_WARNING_HOURS = 21

MONTHLY_OT_LIMIT_HOURS = 25

MONTHLY_OT_WARNING_MINUTES = (

    MONTHLY_OT_WARNING_HOURS * 60

)

MONTHLY_OT_LIMIT_MINUTES = (

    MONTHLY_OT_LIMIT_HOURS * 60

)

MAX_DAILY_OT_MINUTES = 300

# =====================================================
# Attendance Rules
# =====================================================

CHECK_LATE_IN = True

CHECK_EARLY_OUT = True

CHECK_MISSING_IN = True

CHECK_MISSING_OUT = True

AUTO_CALCULATE_WORKING_HOURS = True

AUTO_CALCULATE_DAILY_OT = True

AUTO_CALCULATE_MONTHLY_OT = True

AUTO_GENERATE_NOTIFICATION = True

# =====================================================
# Daily OT Rules
# =====================================================

DAILY_OT_WARNING = 45

DAILY_OT_LIMIT = 60
# =====================================================
# Monthly Status
# =====================================================

NORMAL_STATUS = "Normal"

WARNING_STATUS = "Warning"

LIMIT_REACHED_STATUS = "Limit Reached"

EXCEEDED_STATUS = "Exceeded"

# =====================================================
# Notification Rules
# =====================================================

SEND_WARNING_AT_21_HOURS = True

SEND_LIMIT_REACHED_AT_25_HOURS = True

SEND_EXCEEDED_NOTIFICATION = True

# =====================================================
# Monthly OT Database Columns
# =====================================================

MONTHLY_DATABASE_COLUMNS = [

    "Employee ID",

    "Employee Name",

    "Department",

    "Designation",

    "Email",

    "Phone"

]

# ------------------------------------------
# Day1 -> Day31
# ------------------------------------------

for day in range(1, 32):

    MONTHLY_DATABASE_COLUMNS.append(
        f"Day{day}"
    )

# ------------------------------------------
# Monthly Information
# ------------------------------------------

MONTHLY_DATABASE_COLUMNS.extend([

    "Monthly OT",

    "Monthly OT Minutes",

    "Remaining OT",

    "Remaining OT Minutes",

    "Monthly Status",

    "Last Updated"

])
# =====================================================
# Attendance Column Detection
# =====================================================

EMPLOYEE_ID_COLUMNS = [
    "Employee No",
    "Employee ID",
    "Emp ID",
    "Emp No",
    "Employee Number"
]

EMPLOYEE_NAME_COLUMNS = [
    "Employee Name",
    "Name",
    "Emp Name"
]

DATE_COLUMNS = [
    "Attendance Date",
    "Date"
]

IN_TIME_COLUMNS = [
    "IN Time",
    "Punch In",
    "In Time",
    "IN"
]

OUT_TIME_COLUMNS = [
    "OUT Time",
    "Punch Out",
    "Out Time",
    "OUT"
]

OT_COLUMNS = [
    "OT HRS",
    "OT",
    "Over Time"
]

LATE_COLUMNS = [
    "Late IN(HH:MM)",
    "Late IN",
    "Late"
]

EARLY_COLUMNS = [
    "Early OUT(HH:MM)",
    "Early OUT",
    "Early"
]

# =====================================================
# Email Configuration
# =====================================================

SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587

SMTP_USERNAME = "adishtam.hr@gmail.com"

SMTP_PASSWORD = os.getenv(
    "EMAIL_PASSWORD",
    ""
)

USE_TLS = True

EMAIL_TIMEOUT = 30

EMAIL_RETRY_COUNT = 3

EMAIL_SUBJECT = "Attendance Notification"

HR_REPORT_SUBJECT = "Daily Attendance Report"

WARNING_SUBJECT = "Monthly OT Warning"

LIMIT_SUBJECT = "Monthly OT Limit Reached"

EXCEEDED_SUBJECT = "Monthly OT Exceeded"

# =====================================================
# Notification Settings
# =====================================================

SEND_TO_EMPLOYEE = True

SEND_TO_HR = True

ENABLE_EMAIL = True

ENABLE_WHATSAPP = True

ENABLE_SMS = False

AUTO_SEND_NOTIFICATION = True

# =====================================================
# Dashboard Settings
# =====================================================

DEFAULT_PAGE_SIZE = 25

ENABLE_SEARCH = True

ENABLE_SORTING = True

ENABLE_PAGINATION = True

SHOW_DASHBOARD_CHARTS = True

SHOW_EMPLOYEE_TABLE = True

SHOW_PROGRESS_BAR = True

SHOW_FILTER_BUTTONS = True

SHOW_EMPLOYEE_SEARCH = True

# =====================================================
# Flask Configuration
# =====================================================

FLASK_CONFIG = {

    "SECRET_KEY": SECRET_KEY,

    "UPLOAD_FOLDER": UPLOAD_FOLDER,

    "REPORT_FOLDER": REPORT_FOLDER,

    "MAX_CONTENT_LENGTH": MAX_CONTENT_LENGTH,

    "DEBUG": DEBUG

}

# =====================================================
# Configuration Validation
# =====================================================

if MONTHLY_OT_LIMIT_MINUTES <= 0:

    raise ValueError(
        "Invalid Monthly OT Limit."
    )

if MAX_CONTENT_LENGTH <= 0:

    raise ValueError(
        "Invalid Upload Size."
    )

# =====================================================
# End of Configuration
# =====================================================