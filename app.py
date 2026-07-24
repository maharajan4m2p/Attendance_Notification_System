"""
=========================================================
Attendance Notification System Pro
Main Flask Application
Version : 10.0 Enterprise
=========================================================
"""

import os
import logging
import traceback

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
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

app.secret_key = SECRET_KEY

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["REPORT_FOLDER"] = REPORT_FOLDER

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
# =====================================================
# Create Required Folders
# =====================================================

REQUIRED_FOLDERS = (

    app.config["UPLOAD_FOLDER"],

    app.config["REPORT_FOLDER"]

)

for folder in REQUIRED_FOLDERS:

    os.makedirs(

        folder,

        exist_ok=True

    )

# =====================================================
# Initialize Services
# =====================================================

attendance_checker = AttendanceChecker()

report_generator = ReportGenerator()

notification_service = NotificationService()

email_service = EmailService()

logger.info("All services initialized successfully.")

# =====================================================
# Global Runtime Variables
# =====================================================

analysis_result = None

report_path = None

uploaded_file = None

# =====================================================
# Application Startup
# =====================================================

logger.info("=" * 60)

logger.info(APP_NAME)

logger.info(f"Version : {VERSION}")

logger.info("Application initialized successfully.")

logger.info("=" * 60)
# =====================================================
# Utility Functions
# =====================================================

def allowed_file(filename):
    """
    Check whether the uploaded file extension is allowed.
    """

    if not filename:

        return False

    if "." not in filename:

        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """
    Save uploaded file securely.

    Returns:
        str : Saved file path
    """

    filename = secure_filename(file.filename)

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )

    file.save(filepath)

    logger.info(

        f"Uploaded file saved : {filepath}"

    )

    return filepath


def get_employees():
    """
    Return employee list safely.
    """

    global analysis_result

    if analysis_result is None:

        return []

    return analysis_result.get(

        "employees",

        []

    )


def get_summary():
    """
    Return attendance summary safely.
    """

    global analysis_result

    if analysis_result is None:

        return {}

    return analysis_result.get(

        "summary",

        {}

    )
    # =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    return render_template(

        "index.html",

        app_name=APP_NAME,

        version=VERSION

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
    global uploaded_file

    try:

        # -----------------------------------------
        # Validate Upload
        # -----------------------------------------

        if "attendance_file" not in request.files:

            flash("Please select an attendance file.")

            return redirect(

                url_for("home")

            )

        file = request.files["attendance_file"]

        if file.filename is None or file.filename.strip() == "":

            flash("No file selected.")

            return redirect(

                url_for("home")

            )

        if not allowed_file(file.filename):

            flash(

                "Only .xlsx, .xls and .csv files are supported."

            )

            return redirect(

                url_for("home")

            )

        # -----------------------------------------
        # Save Uploaded File
        # -----------------------------------------

        uploaded_file = save_uploaded_file(

            file

        )

        logger.info(

            "Attendance processing started."

        )

        # -----------------------------------------
        # Attendance Processing
        # -----------------------------------------

        analysis_result = attendance_checker.process_excel(

            uploaded_file

        )

        employees = analysis_result.get(

            "employees",

            []

        )

        # -----------------------------------------
        # Generate Employee Notifications
        # -----------------------------------------

        for employee in employees:

            employee["notification"] = (

                notification_service.generate_message(

                    employee

                )

            )

        # -----------------------------------------
        # Generate Excel Report
        # -----------------------------------------

        report_path = report_generator.generate_excel(

            employees,

            "Attendance_Report.xlsx"

        )

        logger.info(

            "Attendance processing completed successfully."

        )

        flash(

            f"Attendance processed successfully. Total Employees: {len(employees)}"

        )

        return redirect(

            url_for("dashboard")

        )

    except Exception as error:

        logger.exception(

            "Attendance processing failed."

        )

        traceback.print_exc()

        flash(

            f"Processing Failed: {error}"

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

    if analysis_result is None:

        flash(

            "Please upload an attendance file first."

        )

        return redirect(

            url_for("home")

        )

    summary = get_summary()

    employees = analysis_result.get("employees", [])

    print("=" * 60)
    print("SUMMARY")
    print(summary)
    print("=" * 60)

    print("=" * 60)
    print(f"Original Records : {len(get_employees())}")
    print(f"Dashboard Employees : {len(employees)}")
    print("=" * 60)

    print("=" * 60)
    print("Top 5 Employees")
    for emp in employees[:5]:
        print(
            emp["employee_id"],
            emp["name"],
            emp["monthly_ot"],
            emp["monthly_status"]
        )
    print("=" * 60)

    logger.info(

        f"Dashboard opened | Employees : {len(employees)}"

    )

    return render_template(

        "dashboard.html",

        app_name=APP_NAME,

        version=VERSION,

        result=analysis_result,

        summary=summary,

        employees=employees,

        hr_report=analysis_result.get(

            "hr_report",

            ""

        ),

        late_punch_report=analysis_result.get(

            "late_punch_report",

            ""

        ),

        report_generated=report_path is not None

    )
    # =====================================================
# Download Excel Report
# =====================================================

@app.route("/download")
def download_report():

    global report_path

    if not report_path:

        flash(

            "Attendance report has not been generated yet."

        )

        return redirect(

            url_for("dashboard")

        )

    if not os.path.exists(report_path):

        logger.error(

            f"Report file not found : {report_path}"

        )

        flash(

            "Report file not found."

        )

        return redirect(

            url_for("dashboard")

        )

    logger.info(

        f"Downloading report : {report_path}"

    )

    return send_file(

        report_path,

        as_attachment=True,

        download_name=os.path.basename(

            report_path

        )

    )


# =====================================================
# Send Employee Emails
# =====================================================

@app.route(

    "/send_emails",

    methods=["POST"]

)
def send_emails():

    global analysis_result

    if analysis_result is None:

        flash(

            "Please upload an attendance file first."

        )

        return redirect(

            url_for("home")

        )

    employees = get_employees()

    if not employees:

        flash(

            "No employee records available."

        )

        return redirect(

            url_for("dashboard")

        )

    logger.info(

        f"Sending emails to {len(employees)} employees."

    )

    try:

        result = email_service.send_batch(

            employees

        )

        logger.info(

            f"Email Summary : {result}"

        )

        flash(

            f"Email Completed | "

            f"Sent : {result['sent']} | "

            f"Failed : {result['failed']} | "

            f"Skipped : {result['skipped']} | "

            f"Success : {result['success_rate']}%"

        )

    except Exception:

        logger.exception(

            "Email sending failed."

        )

        flash(

            "Failed to send employee emails."

        )

    return redirect(

        url_for("dashboard")

    )
    # =====================================================
# Error Handlers
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    logger.warning(

        f"404 Error : {request.path}"

    )

    return (

        render_template(

            "404.html",

            app_name=APP_NAME,

            version=VERSION

        ),

        404

    )


@app.errorhandler(500)
def internal_server_error(error):

    logger.exception(

        "Internal Server Error"

    )

    traceback.print_exc()

    return (

        render_template(

            "500.html",

            app_name=APP_NAME,

            version=VERSION,

            error=str(error)

        ),

        500

    )


# =====================================================
# Health Check
# =====================================================

@app.route("/health")
def health():

    return {

        "status": "OK",

        "application": APP_NAME,

        "version": VERSION

    }, 200


# =====================================================
# Application Information API
# =====================================================

@app.route("/info")
def application_info():

    return {

        "application": APP_NAME,

        "version": VERSION,

        "status": "Running"

    }, 200
    # =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":

    logger.info("=" * 60)

    logger.info(APP_NAME)

    logger.info(f"Version : {VERSION}")

    logger.info("Attendance Notification System Pro Started")

    logger.info(f"Host : {HOST}")

    logger.info(f"Port : {PORT}")

    logger.info("=" * 60)

    app.run(

        host=HOST,

        port=PORT,

        debug=DEBUG,

        threaded=True,

        use_reloader=False

    )