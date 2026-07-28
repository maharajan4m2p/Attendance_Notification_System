"""
=========================================================
Attendance Notification System Pro
Main Flask Application
Version : 13.0 Enterprise
Developed by Maharajan
=========================================================
"""

import logging
import os
import traceback

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for
)

from werkzeug.utils import secure_filename

from config import (
    APP_NAME,
    VERSION,
    SECRET_KEY,
    DEBUG,
    HOST,
    PORT,
    UPLOAD_FOLDER,
    REPORT_FOLDER,
    ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH
)

from services.attendance_checker import AttendanceChecker
from services.report_generator import ReportGenerator
from services.notification_service import NotificationService
from services.email_service import EmailService
from services.database_manager import DatabaseManager
from services.hr_report import HRReportGenerator
from services.overtime_manager import OvertimeManager
# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# Flask Application
# =====================================================

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config.update(
    SECRET_KEY=SECRET_KEY,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    REPORT_FOLDER=REPORT_FOLDER,
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH
)

# =====================================================
# Create Required Folders
# =====================================================

for folder in (
    UPLOAD_FOLDER,
    REPORT_FOLDER
):
    os.makedirs(
        folder,
        exist_ok=True
    )

# =====================================================
# Initialize Enterprise Services
# =====================================================

attendance_checker = AttendanceChecker()

database_manager = DatabaseManager()

report_generator = ReportGenerator()

notification_service = NotificationService()

email_service = EmailService()

hr_report_generator = HRReportGenerator()

overtime_manager = OvertimeManager()

logger.info("=" * 70)
logger.info(APP_NAME)
logger.info(f"Version : {VERSION}")
logger.info("Enterprise Services Initialized Successfully")
logger.info("=" * 70)

# =====================================================
# Runtime Variables
# =====================================================

analysis_result = None

report_path = None

monthly_report_path = None

database_report_path = None

uploaded_file = None
# =====================================================
# Utility Functions
# =====================================================

def allowed_file(filename):
    """
    Validate uploaded file extension.
    """

    return (

        filename

        and "." in filename

        and filename.rsplit(".", 1)[1].lower()

        in ALLOWED_EXTENSIONS

    )


# =====================================================
# Save Uploaded File
# =====================================================

def save_uploaded_file(file):

    filename = secure_filename(

        file.filename

    )

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )

    file.save(filepath)

    logger.info(

        f"Uploaded File : {filepath}"

    )

    return filepath


# =====================================================
# Get Employees
# =====================================================

def get_employees():

    global analysis_result

    if analysis_result is None:

        return []

    return analysis_result.get(

        "employees",

        []

    )


# =====================================================
# Get Summary
# =====================================================

def get_summary():

    global analysis_result

    if analysis_result is None:

        return {}

    return analysis_result.get(

        "summary",

        {}

    )


# =====================================================
# Get Dashboard
# =====================================================

def get_dashboard():

    global analysis_result

    if analysis_result is None:

        return database_manager.get_dashboard_summary()

    return analysis_result.get(

        "dashboard",

        database_manager.get_dashboard_summary()

    )


# =====================================================
# Get HR Report
# =====================================================

def get_hr_report():

    global analysis_result

    if analysis_result is None:

        return ""

    return analysis_result.get(

        "hr_report",

        ""

    )


# =====================================================
# Get Late Punch Report
# =====================================================

def get_late_punch_report():

    global analysis_result

    if analysis_result is None:

        return ""

    return analysis_result.get(

        "late_punch_report",

        ""

    )


# =====================================================
# Get WhatsApp Report
# =====================================================

def get_whatsapp_report():

    global analysis_result

    if analysis_result is None:

        return ""

    return analysis_result.get(

        "whatsapp_hr_report",

        ""

    )


# =====================================================
# Reset Runtime
# =====================================================

def reset_runtime():

    global analysis_result
    global report_path
    global monthly_report_path
    global database_report_path
    global uploaded_file

    analysis_result = None

    report_path = None

    monthly_report_path = None

    database_report_path = None

    uploaded_file = None
    # =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    dashboard = database_manager.get_dashboard_summary()

    return render_template(

        "index.html",

        app_name=APP_NAME,

        version=VERSION,

        dashboard=dashboard

    )


# =====================================================
# Upload Attendance File
# =====================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_file():

    global analysis_result
    global report_path
    global monthly_report_path
    global database_report_path
    global uploaded_file

    try:

        # -----------------------------------------
        # Validate Upload
        # -----------------------------------------

        if "attendance_file" not in request.files:

            flash(
                "Please select an attendance file.",
                "warning"
            )

            return redirect(url_for("home"))

        file = request.files["attendance_file"]

        if file.filename == "":

            flash(
                "No file selected.",
                "warning"
            )

            return redirect(url_for("home"))

        if not allowed_file(file.filename):

            flash(
                "Only XLSX, XLS and CSV files are supported.",
                "danger"
            )

            return redirect(url_for("home"))

        # -----------------------------------------
        # Save Uploaded File
        # -----------------------------------------

        uploaded_file = save_uploaded_file(file)

        logger.info(
            f"Processing : {uploaded_file}"
        )

        # -----------------------------------------
        # Process Attendance
        # -----------------------------------------

        analysis_result = attendance_checker.process_excel(
            uploaded_file
        )

        employees = analysis_result.get(
            "employees",
            []
        )

        summary = analysis_result.get(
            "summary",
            {}
        )

        # -----------------------------------------
        # Generate Notifications
        # -----------------------------------------

        for employee in employees:

            employee["notification"] = (

                notification_service.generate_message(
                    employee
                )

            )

        # -----------------------------------------
        # Attendance Report
        # -----------------------------------------

        report_path = report_generator.generate_excel(

            employees,

            "Attendance_Report.xlsx"

        )

        # -----------------------------------------
        # Monthly OT Report
        # -----------------------------------------

        monthly_report_path = (

            report_generator.generate_monthly_ot_report(

                employees,

                "Monthly_OT_Report.xlsx"

            )

        )

        # -----------------------------------------
        # Monthly Database Export
        # -----------------------------------------

        database_report_path = (

            report_generator.export_monthly_database(

                "Monthly_OT_Database.xlsx"

            )

        )

        logger.info("=" * 70)

        logger.info(
            f"Employees : {len(employees)}"
        )

        logger.info(
            f"Present : {summary.get('present',0)}"
        )

        logger.info(
            f"Overtime : {summary.get('overtime',0)}"
        )

        logger.info("=" * 70)

        flash(

            f"Attendance processed successfully. {len(employees)} employees processed.",

            "success"

        )

        return redirect(

            url_for("dashboard")

        )

    except Exception as error:

        logger.exception(error)

        traceback.print_exc()

        flash(

            f"Processing Failed : {error}",

            "danger"

        )

        return redirect(

            url_for("home")

        )
        # =====================================================
# Dashboard
# =====================================================

@app.route("/dashboard")
def dashboard():

    global analysis_result
    global report_path
    global monthly_report_path
    global database_report_path
    
    status = request.args.get("status","All")

    if analysis_result is None:

        flash(
            "Please upload an attendance file first.",
            "warning"
        )

        return redirect(
            url_for("home")
        )

    # -----------------------------------------
    # Load Data
    # -----------------------------------------

    employees = get_employees()
    
    if status != "All":
        
        employees = [
            
            employee
            
            for employee in employees
            
            if employee.get("monthly_status") == status
            
        ]

    summary = get_summary()

    dashboard = get_dashboard()

    hr_report = get_hr_report()

    late_punch_report = get_late_punch_report()

    whatsapp_report = get_whatsapp_report()

    # -----------------------------------------
    # Sort by Monthly OT
    # -----------------------------------------

    top_ot = sorted(

        employees,

        key=lambda employee: employee.get(

            "monthly_ot_minutes",

            0

        ),

        reverse=True

    )[:10]

    # -----------------------------------------
    # Top OT Employees
    # -----------------------------------------

    # -----------------------------------------
    # Dashboard Logging
    # -----------------------------------------

    logger.info("=" * 70)

    logger.info("Dashboard Loaded Successfully")

    logger.info(f"Employees            : {len(employees)}")

    logger.info(f"Present              : {summary.get('present',0)}")

    logger.info(f"Absent               : {summary.get('absent',0)}")

    logger.info(f"Late Punch           : {summary.get('late_in',0)}")

    logger.info(f"Early Out            : {summary.get('early_out',0)}")

    logger.info(f"Missing Punch In     : {summary.get('missing_in',0)}")

    logger.info(f"Missing Punch Out    : {summary.get('missing_out',0)}")

    logger.info(f"Overtime Employees   : {summary.get('overtime',0)}")

    logger.info(f"Monthly Warning      : {summary.get('monthly_warning',0)}")

    logger.info(f"Limit Reached        : {summary.get('monthly_limit_reached',0)}")

    logger.info(f"OT Exceeded          : {summary.get('monthly_ot_exceeded',0)}")

    logger.info("=" * 70)

    # -----------------------------------------
    # Render Dashboard
    # -----------------------------------------

    return render_template(

        "dashboard.html",

        app_name=APP_NAME,

        version=VERSION,

        employees=employees,

        summary=summary,

        dashboard=dashboard,

        top_ot=top_ot,

        hr_report=hr_report,

        late_punch_report=late_punch_report,

        whatsapp_report=whatsapp_report,

        attendance_report=report_path,

        monthly_report=monthly_report_path,

        database_report=database_report_path,

        report_generated=(report_path is not None),
        
        selected_status=status

    )
    # =====================================================
# Download Attendance Report
# =====================================================

@app.route("/download")
def download_report():
    
    global analysis_result
    
    status = request.args.get("status","All")

    if analysis_result is None:
        
        flash("Upload attendance first","warning")
        
        return redirect(url_for("home"))
    
    employees = analysis_result["employees"]
    
    if status != "All":
        
        employees = [
            
            employee
            
            for  employee in employees
            
            if employee["monthly_status"] == status
                
        ]
        
        report = report_generator.generate_excel(
            
            employees,
            
            "Attendance_Report.xlsx"
        )
        
        return send_file(
            
            report,
            
            as_attachment=True,
            
            download_name="Attendance_Report.xlsx"
        )


# =====================================================
# Download Monthly OT Report
# =====================================================

# =====================================================
# Download Monthly OT Report
# =====================================================

@app.route("/download_monthly")
def download_monthly():

    global analysis_result

    status = request.args.get("status", "All")

    if analysis_result is None:

        flash("Upload attendance first.", "warning")

        return redirect(url_for("home"))

    employees = analysis_result["employees"]

    if status != "All":

        employees = [

            employee

            for employee in employees

            if employee.get("monthly_status") == status

        ]

    report = report_generator.generate_monthly_ot_report(

        employees,

        "Monthly_OT_Report.xlsx"

    )

    return send_file(

        report,

        as_attachment=True,

        download_name="Monthly_OT_Report.xlsx"

    )


# =====================================================
# Download Monthly Database
# =====================================================

# =====================================================
# Download Monthly Database
# =====================================================

@app.route("/download_database")
def download_database():

    global analysis_result

    status = request.args.get("status", "All")

    if analysis_result is None:

        flash("Upload attendance first.", "warning")

        return redirect(url_for("home"))

    employees = analysis_result["employees"]

    if status != "All":

        employees = [

            employee

            for employee in employees

            if employee.get("monthly_status") == status

        ]

    report = report_generator.export_monthly_database(

        "Monthly_OT_Database.xlsx",

        employees

    )

    return send_file(

        report,

        as_attachment=True,

        download_name="Monthly_OT_Database.xlsx"

    )


# =====================================================
# Send Employee Emails
# =====================================================

# =====================================================
# Send Employee Emails
# =====================================================

@app.route("/send_emails", methods=["POST"])
def send_batch():

    global analysis_result

    if analysis_result is None:

        flash("Upload attendance first.", "warning")

        return redirect(url_for("home"))

    status = request.args.get("status", "All")

    employees = analysis_result["employees"]

    # -----------------------------------------
    # Filter Employees
    # -----------------------------------------

    if status != "All":

        employees = [

            employee

            for employee in employees

            if employee.get("monthly_status") == status

        ]

    # -----------------------------------------
    # Send Emails
    # -----------------------------------------

    result = email_service.send_batch(

        employees

    )

    flash(

        f"Monthly OT Status : {status} | "

        f"Sent : {result['sent']} | "

        f"Failed : {result['failed']} | "

        f"Skipped : {result['skipped']} | "

        f"Success : {result['success_rate']}%",

        "success"

    )

    return redirect(

        url_for(

            "dashboard",

            status=status

        )

    )


# =====================================================
# Health API
# =====================================================

@app.route("/health")
def health():

    return {

        "status": "OK",

        "application": APP_NAME,

        "version": VERSION

    }


# =====================================================
# Application Information
# =====================================================

@app.route("/info")
def info():

    return {

        "application": APP_NAME,

        "version": VERSION,

        "dashboard": database_manager.get_dashboard_summary()

    }


# =====================================================
# 404 Error
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html",

        app_name=APP_NAME,

        version=VERSION

    ), 404


# =====================================================
# 500 Error
# =====================================================

@app.errorhandler(500)
def internal_error(error):

    logger.exception(error)

    return render_template(

        "500.html",

        app_name=APP_NAME,

        version=VERSION,

        error=str(error)

    ), 500


# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":

    logger.info("=" * 70)

    logger.info(APP_NAME)

    logger.info(f"Version : {VERSION}")

    logger.info("Attendance Notification System Started")

    logger.info("=" * 70)

    app.run(

        host=HOST,

        port=PORT,

        debug=DEBUG,

        threaded=True,

        use_reloader=False

    )