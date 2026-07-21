"""
=========================================================
Attendance Notification System Pro
Enterprise Version 5.0
Developed by Maharajan

Features
---------------------------------------------------------
✔ Daily Attendance Analysis
✔ Late Punch Detection
✔ Early Out Detection
✔ Missing Punch Detection
✔ Daily Overtime Calculation
✔ Monthly Overtime Tracking
✔ Monthly OT History Database
✔ Warning Notifications
✔ 25 Hours Monthly OT Limit
✔ Dashboard Analytics
✔ Excel Report Generation
=========================================================
"""

import os
# =====================================================
# Application Configuration
# =====================================================

APP_NAME = "Attendance Notification System Pro"

VERSION = "5.0 Enterprise"

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
# Create Required Folders Automatically
# =====================================================

for folder in [

    UPLOAD_FOLDER,

    REPORT_FOLDER,

    DATABASE_FOLDER,

    LOG_FOLDER,

    BACKUP_FOLDER

]:

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
# Upload Settings
# =====================================================

ALLOWED_EXTENSIONS = {

    "xlsx",

    "xls",

    "csv"

}

MAX_CONTENT_LENGTH = 20 * 1024 * 1024      # 20 MB

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

# Monthly Status

NORMAL_STATUS = "Normal"

WARNING_STATUS = "Warning"

LIMIT_REACHED_STATUS = "Limit Reached"

EXCEEDED_STATUS = "Exceeded"

# Monthly History

STORE_MONTHLY_HISTORY = True

AUTO_MONTH_RESET = True

AUTO_BACKUP_DATABASE = True

# Notification Rules

SEND_WARNING_AT_21_HOURS = True

SEND_LIMIT_REACHED_AT_25_HOURS = True

SEND_EXCEEDED_NOTIFICATION = True

SEND_NOTIFICATION_ONCE = True

# Dashboard

SHOW_REMAINING_OT = True

SHOW_LIMIT_REACHED = True

SHOW_OT_EXCEEDED = True

SHOW_PROGRESS_BAR = True

SHOW_MONTHLY_HISTORY = True

# Employee History

KEEP_ALL_HISTORY = True

REMOVE_DUPLICATE_DATE = True

UPDATE_EXISTING_RECORD = True
# =====================================================
# Date & Time Format
# =====================================================

DATE_FORMAT = "%d-%b-%Y"

TIME_FORMAT = "%I:%M %p"

DATETIME_FORMAT = "%d-%b-%Y %I:%M %p"

DATABASE_DATE_FORMAT = "%Y-%m-%d"

DATABASE_MONTH_FORMAT = "%Y-%m"

# =====================================================
# Notification Settings
# =====================================================

ENABLE_EMAIL = True

ENABLE_WHATSAPP = True

ENABLE_SMS = False

ENABLE_TEAMS = False

AUTO_SEND_NOTIFICATION = True

SEND_DAILY_NOTIFICATION = True

SEND_MONTHLY_NOTIFICATION = True

SEND_WARNING_EMAIL = True

SEND_LIMIT_EMAIL = True

SEND_EXCEEDED_EMAIL = True

SEND_WARNING_WHATSAPP = True

SEND_LIMIT_WHATSAPP = True

SEND_EXCEEDED_WHATSAPP = True

SEND_TO_HR = True

SEND_TO_EMPLOYEE = True

NOTIFY_ONLY_ON_STATUS_CHANGE = True
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

EMAIL_ADDRESS = "adishtam.hr@gmail.com"

EMAIL_PASSWORD = os.getenv(

    "EMAIL_PASSWORD",

    ""

)

USE_TLS = True

EMAIL_TIMEOUT = 30

EMAIL_RETRY_COUNT = 3

EMAIL_SUBJECT = "Attendance Notification"

HR_REPORT_SUBJECT = "Daily Attendance Report"

WARNING_SUBJECT = "Monthly Overtime Warning"

LIMIT_SUBJECT = "Monthly Overtime Limit Reached"

EXCEEDED_SUBJECT = "Monthly Overtime Exceeded"
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
# Application Information
# =====================================================

VERSION = "5.0 Enterprise"

AUTHOR = "Maharajan"

COPYRIGHT = "Attendance Notification System Pro"

LAST_UPDATED = "2026"

BUILD = "Enterprise Release"