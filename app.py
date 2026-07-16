"""
=========================================================
Attendance Notification System Pro
Main Flask Application
Version : 2.0
Developed by Maharajan
=========================================================
"""

import os

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
from services.hr_report import HRReportGenerator
from services.email_service import EmailService


# =========================================================
# Flask Application
# =========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER


# =========================================================
# Services
# =========================================================

attendance_checker = AttendanceChecker()

report_generator = ReportGenerator()

hr_report_generator = HRReportGenerator()

email_service = EmailService()


# =========================================================
# Global Variables
# =========================================================

analysis_result = None

report_path = None

hr_report = ""
# =========================================================
# Utility Functions
# =========================================================

def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =========================================================
# Home Page
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        app_name=APP_NAME
    )
    # =========================================================
# Upload Attendance Excel
# =========================================================

@app.route("/upload", methods=["POST"])
def upload_file():

    global analysis_result
    global report_path
    global hr_report

    if "attendance_file" not in request.files:

        flash("Please select an Excel file.")

        return redirect(url_for("home"))

    file = request.files["attendance_file"]

    if file.filename == "":

        flash("No file selected.")

        return redirect(url_for("home"))

    if not allowed_file(file.filename):

        flash("Only Excel (.xlsx or .xls) files are allowed.")

        return redirect(url_for("home"))

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    try:

        # ==========================================
        # Process Attendance
        # ==========================================

        analysis_result = attendance_checker.process_excel(
            filepath
        )

        # ==========================================
        # Generate Excel Report
        # ==========================================

        report_path = report_generator.generate_report(
            analysis_result,
            filename
        )

        # ==========================================
        # Generate HR WhatsApp Report
        # ==========================================

        hr_report = hr_report_generator.generate(
            analysis_result["employees"],
            analysis_result["summary"]
        )

        # ==========================================
        # Send Email Notifications
        # ==========================================

        sent = 0
        failed = 0

        for employee in analysis_result["employees"]:

            email = employee.get("email", "").strip()

            if email:

                if email_service.send_email(employee):

                    sent += 1

                else:

                    failed += 1

        flash(
            f"Attendance processed successfully. "
            f"Emails Sent : {sent} | Failed : {failed}"
        )

        return redirect(
            url_for("dashboard")
        )

    except Exception as e:

        flash(str(e))

        return redirect(
            url_for("home")
        )
        # =========================================================
# Dashboard
# =========================================================

@app.route("/dashboard")
def dashboard():

    global analysis_result
    global hr_report

    if analysis_result is None:

        flash(
            "Please upload an attendance Excel file first."
        )

        return redirect(
            url_for("home")
        )

    return render_template(

        "dashboard.html",

        app_name=APP_NAME,

        result=analysis_result,

        hr_report=hr_report

    )


# =========================================================
# Download Excel Report
# =========================================================

@app.route("/download")
def download_report():

    global report_path

    if report_path is None:

        flash(
            "No report available."
        )

        return redirect(
            url_for("dashboard")
        )

    return send_file(

        report_path,

        as_attachment=True

    )


# =========================================================
# Error Handler
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html",

        app_name=APP_NAME

    ), 404


# =========================================================
# Run Application
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )