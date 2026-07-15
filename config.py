"""
=============================================
Attendance Notification System
Configuration File
=============================================
"""

import os

# ==============================
# Application
# ==============================

APP_NAME = "Attendance Notification System"

SECRET_KEY = "attendance_notification_secret_key"

# ==============================
# Folder Paths
# ==============================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

# Allowed Upload Extensions

ALLOWED_EXTENSIONS = {"xlsx", "xls"}

# ==============================
# Company Shift Timings
# ==============================

SHIFT_IN = "09:00"

SHIFT_OUT = "18:00"

# ==============================
# Rules
# ==============================

ALLOW_EARLY_IN = True

CALCULATE_OVERTIME = True

CHECK_MISSING_IN = True

CHECK_MISSING_OUT = True

CHECK_EARLY_OUT = True

CHECK_LATE_IN = True

# ==============================
# Notification
# ==============================

ENABLE_EMAIL = False

ENABLE_SMS = False

ENABLE_WHATSAPP = False

ENABLE_TEAMS = False

# ==============================
# Report
# ==============================

GENERATE_EXCEL_REPORT = True

GENERATE_SUMMARY = True

# ==============================
# Auto Create Folders
# ==============================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(REPORT_FOLDER, exist_ok=True)