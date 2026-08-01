"""
=========================================================
Attendance Notification System Pro
Main Flask Application
Version : 16.0 Enterprise
Developed by Maharajan
=========================================================
"""

import os
import logging
import traceback
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    jsonify
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
from services.database_manager import DatabaseManager
from services.report_generator import ReportGenerator
from services.notification_service import NotificationService
from services.email_service import EmailService
from services.hr_report import HRReportGenerator
from services.overtime_manager import OvertimeManager

# =====================================================
# Logging Configuration
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

app.config["SECRET_KEY"] = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

app.secret_key = SECRET_KEY

# =====================================================
# Create Required Folders
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

uploaded_file = None

report_path = None

monthly_report_path = None

database_report_path = None

current_status_filter = "All"

current_department_filter = "All"

current_designation_filter = "All"

# =====================================================
# End of Part 1
# =====================================================
# =====================================================
# Utility Functions
# =====================================================

def allowed_file(filename):
    """
    Check whether uploaded file has a valid extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =====================================================
# Save Uploaded File
# =====================================================

def save_uploaded_file(file):

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    logger.info(f"Uploaded File : {filepath}")

    return filepath


# =====================================================
# Runtime Data Access
# =====================================================

def get_employees():

    global analysis_result

    if analysis_result is None:
        return []

    return analysis_result.get(
        "employees",
        []
    )


def get_summary():

    global analysis_result

    if analysis_result is None:
        return {}

    return analysis_result.get(
        "summary",
        {}
    )


def get_dashboard():

    global analysis_result

    if analysis_result is None:
        return database_manager.get_dashboard_summary()

    return analysis_result.get(
        "dashboard",
        database_manager.get_dashboard_summary()
    )


def get_hr_report():

    global analysis_result

    if analysis_result is None:
        return ""

    return analysis_result.get(
        "summary",
        {}
    ).get(
        "hr_report",
        ""
    )


def get_notification_summary():

    global analysis_result

    if analysis_result is None:
        return ""

    return analysis_result.get(
        "summary",
        {}
    ).get(
        "notification_summary",
        ""
    )


def get_late_punch_report():

    global analysis_result

    if analysis_result is None:
        return []

    return analysis_result.get(
        "late_employees",
        []
    )


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
    global uploaded_file
    global report_path
    global monthly_report_path
    global database_report_path

    analysis_result = None
    uploaded_file = None
    report_path = None
    monthly_report_path = None
    database_report_path = None

    logger.info("Runtime Reset Completed")
    # =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    dashboard = database_manager.get_dashboard_summary()

    return render_template(

        "index.html",

        app_name=APP_NAME,

        app_version=VERSION,

        current_year=datetime.now().year,

        dashboard=dashboard

    )


# =====================================================
# Upload Attendance File
# =====================================================

@app.route("/upload", methods=["POST"])
def upload_file():

    global analysis_result
    global uploaded_file
    global report_path
    global monthly_report_path
    global database_report_path

    try:

        # ------------------------------------------
        # Validate Upload
        # ------------------------------------------

        if "attendance_file" not in request.files:

            flash(
                "Please choose an attendance file.",
                "warning"
            )

            return redirect(
                url_for("home")
            )

        file = request.files["attendance_file"]

        if file.filename == "":

            flash(
                "No file selected.",
                "warning"
            )

            return redirect(
                url_for("home")
            )

        if not allowed_file(file.filename):

            flash(
                "Only CSV, XLS and XLSX files are supported.",
                "danger"
            )

            return redirect(
                url_for("home")
            )

        # ------------------------------------------
        # Save Upload
        # ------------------------------------------

        uploaded_file = save_uploaded_file(file)

        logger.info(
            f"Processing : {uploaded_file}"
        )

        # ------------------------------------------
        # Process Attendance
        # ------------------------------------------

        analysis_result = attendance_checker.process_excel(
            uploaded_file
        )
        print("=" * 60)
        print("EMPLOYEE FROM PROCESS")
        print("=" * 60)

        employees = []

        for emp in analysis_result.get("employees", []):
            db_emp = database_manager.get_employee(emp["employee_id"])

            if db_emp:
                employee = emp.copy()

                # Copy Day1-Day31
                for i in range(1, 32):
                    employee[f"Day{i}"] = db_emp.get(f"Day{i}", "00:00")

                # Copy monthly values
                employee["monthly_ot"] = db_emp.get("Monthly OT", "00:00")
                employee["monthly_ot_minutes"] = db_emp.get("Monthly OT Minutes", 0)
                employee["remaining_ot"] = db_emp.get("Remaining OT", "25:00")
                employee["remaining_ot_minutes"] = db_emp.get("Remaining OT Minutes", 1500)
                employee["monthly_status"] = db_emp.get("Monthly Status", "Normal")

                employees.append(employee)
                
        analysis_result["employees"] = employees

        summary = analysis_result.get(
            "summary",
            {}
        )

        # ------------------------------------------
        # Generate Notifications
        # ------------------------------------------

        for employee in employees:

            employee["notification"] = (
                notification_service.generate_message(
                    employee
                )
            )

        # ------------------------------------------
        # Generate Reports
        # ------------------------------------------

        report_path = report_generator.generate_excel(
            employees,
            "Attendance_Report.xlsx"
        )

        monthly_report_path = (
            report_generator.generate_monthly_ot_report(
                employees,
                "Monthly_OT_Report.xlsx"
            )
        )

        database_report_path = (
            report_generator.export_monthly_database(
                "Monthly_OT_Database.xlsx"
            )
        )

        logger.info("=" * 70)
        logger.info("Attendance Processing Completed")
        logger.info(f"Employees : {len(employees)}")
        logger.info(f"Present   : {summary.get('present',0)}")
        logger.info(f"Absent    : {summary.get('absent',0)}")
        logger.info(f"Late      : {summary.get('late_in',0)}")
        logger.info(f"Early Out : {summary.get('early_out',0)}")
        logger.info(f"OT        : {summary.get('overtime',0)}")
        logger.info("=" * 70)

        flash(
            f"Attendance processed successfully. "
            f"{len(employees)} employees processed.",
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

    if analysis_result is None:

        flash(
            "Please upload an attendance file first.",
            "warning"
        )

        return redirect(
            url_for("home")
        )

    # =====================================================
    # Filters
    # =====================================================

    status = request.args.get(
        "status",
        "All"
    )

    department = request.args.get(
        "department",
        "All"
    )

    designation = request.args.get(
        "designation",
        "All"
    )

    # =====================================================
    # Load Data
    # =====================================================

    employees = get_employees()

    summary = get_summary()

    dashboard = get_dashboard()

    hr_report = get_hr_report()

    notification_summary = (
        get_notification_summary()
    )

    late_employees = (
        get_late_punch_report()
    )

    whatsapp_report = (
        get_whatsapp_report()
    )

    # =====================================================
    # Apply Filters
    # =====================================================

    filtered = []

    for employee in employees:

        if (
            status != "All"
            and employee.get(
                "monthly_status",
                ""
            ) != status
        ):
            continue

        if (
            department != "All"
            and employee.get(
                "department",
                ""
            ) != department
        ):
            continue

        if (
            designation != "All"
            and employee.get(
                "designation",
                ""
            ) != designation
        ):
            continue

        filtered.append(employee)

    employees = filtered

    # =====================================================
    # Sort by Monthly OT
    # =====================================================

    employees = sorted(

        employees,

        key=lambda employee:
            employee.get(
                "monthly_ot_minutes",
                0
            ),

        reverse=True

    )

    # =====================================================
    # Top 10 Employees
    # =====================================================

    top_ot_employees = employees[:10]
    # =====================================================
    # Dashboard Log
    # =====================================================

    logger.info("=" * 70)
    logger.info("Dashboard Loaded")
    logger.info(f"Employees      : {len(employees)}")
    logger.info(f"Present        : {summary.get('present', 0)}")
    logger.info(f"Absent         : {summary.get('absent', 0)}")
    logger.info(f"Late Punch     : {summary.get('late_in', 0)}")
    logger.info(f"Early Out      : {summary.get('early_out', 0)}")
    logger.info(f"OT Employees   : {summary.get('overtime', 0)}")
    logger.info(f"Warning        : {dashboard.get('monthly_warning', 0)}")
    logger.info(f"Limit Reached  : {dashboard.get('monthly_limit_reached', 0)}")
    logger.info(f"Exceeded       : {dashboard.get('monthly_exceeded', 0)}")
    logger.info("=" * 70)

    # =====================================================
    # Render Dashboard
    # =====================================================

    return render_template(

        "dashboard.html",

        # Application
        app_name=APP_NAME,
        app_version=VERSION,
        current_year=datetime.now().year,

        # Main Data
        employees=employees,
        summary=summary,
        dashboard=dashboard,

        # Reports
        hr_report=hr_report,
        notification_summary=notification_summary,
        late_employees=late_employees,
        whatsapp_report=whatsapp_report,

        # Charts
        top_ot_employees=top_ot_employees,

        # Downloads
        attendance_report=report_path,
        monthly_report=monthly_report_path,
        database_report=database_report_path,

        report_generated=(
            report_path is not None
        ),

        # Selected Filters
        selected_status=status,
        selected_department=department,
        selected_designation=designation
    )
    # =====================================================
# Download Attendance Report
# =====================================================

@app.route("/download")
def download_report():

    global analysis_result

    if analysis_result is None:

        flash(
            "Please upload an attendance file first.",
            "warning"
        )

        return redirect(
            url_for("home")
        )

    status = request.args.get(
        "status",
        "All"
    )

    employees = get_employees()

    if status != "All":

        employees = [

            emp

            for emp in employees

            if emp.get(
                "monthly_status",
                ""
            ) == status

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

@app.route("/download_monthly")
def download_monthly():

    global analysis_result

    if analysis_result is None:

        flash(

            "Please upload an attendance file first.",

            "warning"

        )

        return redirect(

            url_for("home")

        )

    status = request.args.get(

        "status",

        "All"

    )

    employees = get_employees()

    if status != "All":

        employees = [

            emp

            for emp in employees

            if emp.get(

                "monthly_status",

                ""

            ) == status

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

@app.route("/download_database")
def download_database():

    global analysis_result

    if analysis_result is None:

        flash(

            "Please upload an attendance file first.",

            "warning"

        )

        return redirect(

            url_for("home")

        )

    report = report_generator.export_monthly_database(

        "Monthly_OT_Database.xlsx"

    )

    return send_file(

        report,

        as_attachment=True,

        download_name="Monthly_OT_Database.xlsx"

    )
    # =====================================================
# Send Employee Emails
# =====================================================

@app.route("/send_emails", methods=["POST"])
def send_batch():

    global analysis_result

    if analysis_result is None:

        flash(
            "Please upload an attendance file first.",
            "warning"
        )

        return redirect(
            url_for("home")
        )

    status = request.args.get(
        "status",
        "All"
    )

    employees = get_employees()

    if status != "All":

        employees = [

            emp

            for emp in employees

            if emp.get(
                "monthly_status",
                ""
            ) == status

        ]

    result = email_service.send_batch(
        employees
    )

    flash(

        f"Monthly Status : {status} | "
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

    return jsonify({

        "status": "OK",

        "application": APP_NAME,

        "version": VERSION

    })


# =====================================================
# Application Information
# =====================================================

@app.route("/info")
def info():

    return jsonify({

        "application": APP_NAME,

        "version": VERSION,

        "dashboard": database_manager.get_dashboard_summary()

    })


# =====================================================
# 404 Error
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html",

        app_name=APP_NAME,

        app_version=VERSION,

        current_year=datetime.now().year

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

        app_version=VERSION,

        current_year=datetime.now().year,

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