"""
=========================================================
Attendance Notification System Pro
Enterprise Configuration
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""

import os

# =====================================================
# Application Information
# =====================================================

APP_NAME = "Attendance Notification System Pro"

VERSION = "8.0 Enterprise"

AUTHOR = "Maharajan"

SECRET_KEY = "attendance_notification_secret_key"

DEBUG = True

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = os.path.abspath(

    os.path.dirname(__file__)

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

# =====================================================
# Upload Configuration
# =====================================================

ALLOWED_EXTENSIONS = {

    "xlsx",

    "xls",

    "csv"

}

MAX_CONTENT_LENGTH = 20 * 1024 * 1024

SUPPORTED_ENCODINGS = [

    "utf-8",

    "utf-8-sig",

    "latin1",

    "cp1252"

]
# =====================================================
# Company Shift Configuration
# =====================================================

SHIFT_START = "08:30"

SHIFT_END = "17:30"

GRACE_TIME = "08:41"

LUNCH_START = "13:00"

LUNCH_END = "13:30"

STANDARD_WORKING_HOURS = 8

STANDARD_WORKING_MINUTES = 480

WORKING_DAYS_PER_MONTH = 25

# =====================================================
# Attendance Rules
# =====================================================

CHECK_LATE_IN = True

CHECK_EARLY_OUT = True

CHECK_MISSING_IN = True

CHECK_MISSING_OUT = True

CALCULATE_OVERTIME = True

ALLOW_EARLY_IN = True

ALLOW_WEEKEND_OT = True

ALLOW_HOLIDAY_OT = True

AUTO_CALCULATE_WORKING_HOURS = True

AUTO_GENERATE_NOTIFICATION = True

# =====================================================
# Enterprise Overtime Rules
# =====================================================

# Daily OT (Minutes)

DAILY_OT_WARNING = 45

DAILY_OT_LIMIT = 60

MAX_DAILY_OT = 300

# Monthly OT (Hours)

MONTHLY_OT_WARNING = 21

MONTHLY_OT_LIMIT = 25

MONTHLY_OT_MAX = 999

# =====================================================
# Monthly Status
# =====================================================

NORMAL_STATUS = "Normal"

WARNING_STATUS = "Warning"

LIMIT_REACHED_STATUS = "Limit Reached"

EXCEEDED_STATUS = "Exceeded"

# =====================================================
# Monthly Database Rules
# =====================================================

STORE_MONTHLY_HISTORY = True

AUTO_MONTH_RESET = True

AUTO_BACKUP_DATABASE = True

REMOVE_DUPLICATE_DATE = True

UPDATE_EXISTING_RECORD = True

KEEP_ALL_HISTORY = True

# =====================================================
# Notification Rules
# =====================================================

SEND_WARNING_AT_21_HOURS = True

SEND_LIMIT_REACHED_AT_25_HOURS = True

SEND_EXCEEDED_NOTIFICATION = True

SEND_NOTIFICATION_ONCE = True

AUTO_SEND_NOTIFICATION = True

SEND_TO_EMPLOYEE = True

SEND_TO_HR = True

ENABLE_EMAIL = True

ENABLE_WHATSAPP = True

ENABLE_SMS = False

ENABLE_TEAMS = False

# =====================================================
# Date & Time Format
# =====================================================

DATE_FORMAT = "%d-%b-%Y"

TIME_FORMAT = "%I:%M %p"

DATETIME_FORMAT = "%d-%b-%Y %I:%M %p"

DATABASE_DATE_FORMAT = "%Y-%m-%d"

DATABASE_MONTH_FORMAT = "%Y-%m"

# =====================================================
# Company Information
# =====================================================

COMPANY_NAME = "ADISTHAM VENTURES PRIVATE LIMITED"

HR_NAME = "HR Department"

COMPANY_ADDRESS = "Tirupur, Tamil Nadu"

HR_EMAIL = "adishtam.hr@gmail.com"

SUPPORT_EMAIL = "adishtam.hr@gmail.com"
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

EMAIL_SUBJECT = "Attendance Notification"

HR_REPORT_SUBJECT = "Daily Attendance Report"

WARNING_SUBJECT = "Monthly Overtime Warning"

LIMIT_SUBJECT = "Monthly Overtime Limit Reached"

EXCEEDED_SUBJECT = "Monthly Overtime Exceeded"

USE_TLS = True

EMAIL_TIMEOUT = 30

EMAIL_RETRY_COUNT = 3

# =====================================================
# Report Settings
# =====================================================

GENERATE_EXCEL_REPORT = True

GENERATE_PDF_REPORT = False

GENERATE_SUMMARY = True

GENERATE_DAILY_OT_REPORT = True

GENERATE_MONTHLY_OT_REPORT = True

GENERATE_EMPLOYEE_HISTORY = True

GENERATE_HR_REPORT = True

GENERATE_LATE_REPORT = True

GENERATE_WARNING_REPORT = True

GENERATE_LIMIT_REPORT = True

GENERATE_EXCEEDED_REPORT = True

SAVE_REPORT_HISTORY = True

# =====================================================
# Dashboard Settings
# =====================================================

SHOW_DAILY_OT = True

SHOW_MONTHLY_OT = True

SHOW_EMPLOYEE_HISTORY = True

SHOW_OT_WARNING = True

SHOW_LIMIT_REACHED = True

SHOW_OT_EXCEEDED = True

SHOW_REMAINING_OT = True

SHOW_PROGRESS_BAR = True

SHOW_DASHBOARD_CHARTS = True

SHOW_MONTHLY_HISTORY = True

SHOW_EMPLOYEE_SEARCH = True

SHOW_FILTER_BUTTONS = True

SHOW_EXPORT_BUTTON = True

# =====================================================
# Performance Settings
# =====================================================

MAX_EMPLOYEES_PER_BATCH = 500

DATABASE_CACHE = True

ENABLE_MEMORY_OPTIMIZATION = True

ENABLE_PROGRESS_LOG = True

ENABLE_DATABASE_BACKUP = True

ENABLE_AUTO_CLEANUP = True

# =====================================================
# Application Information
# =====================================================

COPYRIGHT = "Attendance Notification System Pro"

LAST_UPDATED = "2026"

BUILD = "Enterprise Release"

# =====================================================
# End of Configuration
# =====================================================
