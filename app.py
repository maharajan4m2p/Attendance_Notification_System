"""
=========================================================
Attendance Notification System Pro
Main Flask Application
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
"""

import os
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
    SECRET_KEY,
    UPLOAD_FOLDER,
    REPORT_FOLDER,
    ALLOWED_EXTENSIONS
)

from services.attendance_checker import AttendanceChecker
from services.report_generator import ReportGenerator
from services.notification_service import NotificationService
from services.email_service import EmailService

# =====================================================
# Flask Application
# =====================================================

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

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
# Initialize Services
# =====================================================

attendance_checker = AttendanceChecker()

report_generator = ReportGenerator()

notification_service = NotificationService()

email_service = EmailService()

# =====================================================
# Global Variables
# =====================================================

analysis_result = None

report_path = None

uploaded_file = None

# =====================================================
# Utility Function
# =====================================================

def allowed_file(filename):

    return (

        filename is not None

        and "." in filename

        and filename.rsplit(

            ".",

            1

        )[1].lower() in ALLOWED_EXTENSIONS

    )

# =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    return render_template(

        "index.html",

        app_name=APP_NAME

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

    # -------------------------------------------------
    # Validate Upload
    # -------------------------------------------------

    if "attendance_file" not in request.files:

        flash(
            "Please select an attendance file."
        )

        return redirect(
            url_for("home")
        )

    file = request.files["attendance_file"]

    if file.filename == "":

        flash(
            "No file selected."
        )

        return redirect(
            url_for("home")
        )

    if not allowed_file(file.filename):

        flash(
            "Only Excel (.xlsx, .xls) or CSV files are allowed."
        )

        return redirect(
            url_for("home")
        )

    # -------------------------------------------------
    # Save File
    # -------------------------------------------------

    filename = secure_filename(
        file.filename or ""
    )

    uploaded_file = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )

    file.save(
        uploaded_file
    )

    # -------------------------------------------------
    # Process Attendance
    # -------------------------------------------------

    try:

        print("=" * 60)
        print("Attendance Processing Started")
        print("=" * 60)

        analysis_result = attendance_checker.process_excel(

            uploaded_file

        )

        employees = analysis_result.get(

            "employees",

            []

        )

        # -------------------------------------------------
        # Generate Notifications
        # -------------------------------------------------

        for employee in employees:

            if not employee.get(
                "notification"
            ):

                employee["notification"] = (

                    notification_service.generate_message(

                        employee

                    )

                )

        # -------------------------------------------------
        # Generate Excel Report
        # -------------------------------------------------

        report_path = report_generator.generate_excel(

            employees,

            "Attendance_Report.xlsx"

        )

        print("=" * 60)
        print("Attendance Processing Completed")
        print("=" * 60)

        flash(
            "Attendance processed successfully."
        )

        return redirect(

            url_for(
                "dashboard"
            )

        )

    except Exception as error:

        traceback.print_exc()

        flash(
            f"Error : {error}"
        )

        return redirect(

            url_for(
                "home"
            )

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

    return render_template(

        "dashboard.html",

        app_name=APP_NAME,

        result=analysis_result,

        hr_report=analysis_result.get(
            "hr_report",
            ""
        ),

        late_punch_report=analysis_result.get(
            "late_punch_report",
            ""
        )

    )

# =====================================================
# Download Excel Report
# =====================================================

@app.route("/download")
def download_report():

    global report_path

    if not report_path:

        flash(
            "No report available."
        )

        return redirect(
            url_for("dashboard")
        )

    if not os.path.exists(report_path):

        flash(
            "Report file not found."
        )

        return redirect(
            url_for("dashboard")
        )

    return send_file(

        report_path,

        as_attachment=True,

        download_name="Attendance_Report.xlsx"

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

    employees = analysis_result.get(
        "employees",
        []
    )

    result = email_service.send_batch(
        employees
    )

    flash(

        f"Emails Sent : {result['sent']} | "

        f"Failed : {result['failed']} | "

        f"Success Rate : {result['success_rate']}%"

    )

    return redirect(
        url_for("dashboard")
    )

# =====================================================
# Error Handlers
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html",

        app_name=APP_NAME

    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    traceback.print_exc()

    return render_template(

        "500.html",

        app_name=APP_NAME,

        error=str(error)

    ), 500

# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print(APP_NAME)
    print("Attendance Notification System Pro Started")
    print("=" * 60)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True,

        threaded=True

    )