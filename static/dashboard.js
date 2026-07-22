/*
=========================================================
Attendance Notification System Pro
Dashboard JavaScript
Version : 10.0 Enterprise
Developed by Maharajan
=========================================================
*/

"use strict";

// =====================================================
// Global Variables
// =====================================================

let hrReportText = "";
let employeeModal = null;

// =====================================================
// Show Employee Details
// =====================================================

function showEmployee(
    id,
    name,
    department,
    designation,
    date,
    punchIn,
    punchOut,
    dailyOT,
    monthlyOT,
    remainingOT,
    dailyStatus,
    monthlyStatus,
    notification
) {

    const setText = (id, value, defaultValue = "--") => {

        const element = document.getElementById(id);

        if (element) {

            element.textContent = value || defaultValue;

        }

    };

    setText("mEmpId", id, "");
    setText("mName", name, "");
    setText("mDepartment", department, "");
    setText("mDesignation", designation, "");
    setText("mDate", date, "");
    setText("mPunchIn", punchIn);
    setText("mPunchOut", punchOut);
    setText("mDailyOT", dailyOT, "00:00");
    setText("mMonthlyOT", monthlyOT, "00:00");
    setText("mRemainingOT", remainingOT, "00:00");
    setText("mDailyStatus", dailyStatus, "Normal");
    setText("mMonthlyStatus", monthlyStatus, "Normal");

    const notificationBox = document.getElementById("mNotification");

    if (notificationBox) {

        notificationBox.value = notification || "";

    }

    // =====================================================
    // Daily Status Badge
    // =====================================================

    const daily = document.getElementById("mDailyStatus");

    if (daily) {

        daily.className = "badge";

        switch (dailyStatus) {

            case "Normal":
                daily.classList.add("bg-success");
                break;

            case "Warning":
                daily.classList.add("bg-warning", "text-dark");
                break;

            case "Limit Reached":
                daily.classList.add("bg-dark");
                break;

            default:
                daily.classList.add("bg-danger");

        }

    }

    // =====================================================
    // Monthly Status Badge
    // =====================================================

    const monthly = document.getElementById("mMonthlyStatus");

    if (monthly) {

        monthly.className = "badge";

        switch (monthlyStatus) {

            case "Normal":
                monthly.classList.add("bg-success");
                break;

            case "Warning":
                monthly.classList.add("bg-warning", "text-dark");
                break;

            case "Limit Reached":
                monthly.classList.add("bg-dark");
                break;

            default:
                monthly.classList.add("bg-danger");

        }

    }

    const modalElement = document.getElementById("employeeModal");

    if (modalElement) {

        employeeModal = new bootstrap.Modal(modalElement);

        employeeModal.show();

    }

}
// =====================================================
// Copy Employee Notification
// =====================================================

async function copyNotification() {

    const notification = document.getElementById("mNotification");

    if (!notification) {
        return;
    }

    try {

        await navigator.clipboard.writeText(notification.value || "");

        alert("Notification copied successfully.");

    } catch (error) {

        console.error(error);

        alert("Failed to copy notification.");

    }

}

// =====================================================
// Add Employee Notification to HR Report
// =====================================================

function addToReport() {

    const notification = document.getElementById("mNotification");
    const hrReport = document.getElementById("hrReport");

    if (!notification || !hrReport) {
        return;
    }

    if (hrReportText.length > 0) {

        hrReportText +=
            "\n\n========================================\n\n";

    }

    hrReportText += notification.value || "";

    hrReport.value = hrReportText;

    alert("Employee added to HR Report.");

}

// =====================================================
// Copy HR Report
// =====================================================

async function copyHRReport() {

    const report = document.getElementById("hrReport");

    if (!report) {
        return;
    }

    try {

        await navigator.clipboard.writeText(report.value || "");

        alert("HR Report copied successfully.");

    } catch (error) {

        console.error(error);

        alert("Failed to copy HR Report.");

    }

}

// =====================================================
// Send HR Report to WhatsApp
// =====================================================

function sendHRReport() {

    const report = document.getElementById("hrReport");

    if (!report || !report.value.trim()) {

        alert("HR Report is empty.");

        return;

    }

    window.open(
        "https://wa.me/?text=" +
        encodeURIComponent(report.value),
        "_blank"
    );

}

// =====================================================
// Copy Late Punch Report
// =====================================================

async function copyLatePunchReport() {

    const report = document.getElementById("latePunchReport");

    if (!report) {
        return;
    }

    try {

        await navigator.clipboard.writeText(report.value || "");

        alert("Late / Missing Punch Report copied.");

    } catch (error) {

        console.error(error);

        alert("Failed to copy report.");

    }

}

// =====================================================
// Send Late Punch Report
// =====================================================

function sendLatePunchReport() {

    const report = document.getElementById("latePunchReport");

    if (!report || !report.value.trim()) {

        alert("Late Punch Report is empty.");

        return;

    }

    window.open(
        "https://wa.me/?text=" +
        encodeURIComponent(report.value),
        "_blank"
    );

}
// =====================================================
// Employee Search
// =====================================================

const employeeSearch = document.getElementById("employeeSearch");

if (employeeSearch) {

    employeeSearch.addEventListener("input", function () {

        const keyword = this.value.toLowerCase().trim();

        const rows = document.querySelectorAll(
            "#employeeTable tbody tr"
        );

        rows.forEach((row) => {

            const text = row.textContent.toLowerCase();

            row.style.display = text.includes(keyword)
                ? ""
                : "none";

        });

    });

}

// =====================================================
// Employee Filters
// =====================================================

const filterButtons = document.querySelectorAll(".filter-btn");

filterButtons.forEach((button) => {

    button.addEventListener("click", function () {

        // Remove Active Class

        filterButtons.forEach((btn) => {

            btn.classList.remove("active");

        });

        this.classList.add("active");

        const filter = this.dataset.filter || "All";

        const rows = document.querySelectorAll(
            "#employeeTable tbody tr"
        );

        rows.forEach((row) => {

            if (filter === "All") {

                row.style.display = "";

                return;

            }

            const text = row.textContent.toLowerCase();

            row.style.display = text.includes(
                filter.toLowerCase()
            )
                ? ""
                : "none";

        });

    });

});

// =====================================================
// Reset Search
// =====================================================

function clearSearch() {

    if (!employeeSearch) {

        return;

    }

    employeeSearch.value = "";

    const rows = document.querySelectorAll(
        "#employeeTable tbody tr"
    );

    rows.forEach((row) => {

        row.style.display = "";

    });

    // Reset Active Filter

    filterButtons.forEach((btn) => {

        btn.classList.remove("active");

        if ((btn.dataset.filter || "") === "All") {

            btn.classList.add("active");

        }

    });

}
// =====================================================
// Dashboard Charts
// =====================================================

window.addEventListener("load", function () {

    const dashboardData = window.dashboardData || {};

    const summary = dashboardData.summary || {};

    const employees = dashboardData.employees || [];

    // =====================================================
    // Attendance Pie Chart
    // =====================================================

    const attendanceCanvas = document.getElementById("attendanceChart");

    if (attendanceCanvas && typeof Chart !== "undefined") {

        new Chart(attendanceCanvas, {

            type: "pie",

            data: {

                labels: [

                    "Present",

                    "Late Punch",

                    "Early Out",

                    "Missing In",

                    "Missing Out"

                ],

                datasets: [{

                    data: [

                        summary.present || 0,

                        summary.late_in || 0,

                        summary.early_out || 0,

                        summary.missing_in || 0,

                        summary.missing_out || 0

                    ],

                    backgroundColor: [

                        "#198754",

                        "#dc3545",

                        "#fd7e14",

                        "#6c757d",

                        "#212529"

                    ]

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });

    }

    // =====================================================
    // Attendance Statistics
    // =====================================================

    const statisticsCanvas = document.getElementById("statisticsChart");

    if (statisticsCanvas && typeof Chart !== "undefined") {

        new Chart(statisticsCanvas, {

            type: "bar",

            data: {

                labels: [

                    "Present",

                    "Late",

                    "Early",

                    "Overtime"

                ],

                datasets: [{

                    label: "Employees",

                    data: [

                        summary.present || 0,

                        summary.late_in || 0,

                        summary.early_out || 0,

                        summary.overtime || 0

                    ],

                    backgroundColor: "#0d6efd"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            precision: 0

                        }

                    }

                }

            }

        });

    }

    // =====================================================
    // Monthly OT Status
    // =====================================================

    const monthlyCanvas = document.getElementById("monthlyOTChart");

    if (monthlyCanvas && typeof Chart !== "undefined") {

        const warning = summary.warning || 0;

        const limit = summary.limit_reached || 0;

        const exceeded = summary.monthly_ot_exceeded || 0;

        const normal = Math.max(

            0,

            (summary.total || 0)

            - warning

            - limit

            - exceeded

        );

        new Chart(monthlyCanvas, {

            type: "doughnut",

            data: {

                labels: [

                    "Normal",

                    "Warning",

                    "Limit Reached",

                    "Exceeded"

                ],

                datasets: [{

                    data: [

                        normal,

                        warning,

                        limit,

                        exceeded

                    ],

                    backgroundColor: [

                        "#198754",

                        "#ffc107",

                        "#212529",

                        "#dc3545"

                    ]

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });

    }

    // =====================================================
    // Top Monthly OT Employees
    // =====================================================

    const topCanvas = document.getElementById("topOTChart");

    if (topCanvas && typeof Chart !== "undefined") {

        const sorted = [...employees]

            .sort(

                (a, b) =>

                    (b.monthly_ot_minutes || 0)

                    -

                    (a.monthly_ot_minutes || 0)

            )

            .slice(0, 10);

        new Chart(topCanvas, {

            type: "bar",

            data: {

                labels: sorted.map(

                    emp => emp.name || "Unknown"

                ),

                datasets: [{

                    label: "Monthly OT (Minutes)",

                    data: sorted.map(

                        emp => emp.monthly_ot_minutes || 0

                    ),

                    backgroundColor: "#6610f2"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis: "y",

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    x: {

                        beginAtZero: true,

                        ticks: {

                            precision: 0

                        }

                    }

                }

            }

        });

    }

});
// =====================================================
// Keyboard Shortcuts
// =====================================================

document.addEventListener(

    "keydown",

    function (event) {

        // Ctrl + F -> Employee Search

        if (

            event.ctrlKey &&

            event.key.toLowerCase() === "f"

        ) {

            event.preventDefault();

            const search = document.getElementById(

                "employeeSearch"

            );

            if (search) {

                search.focus();

                search.select();

            }

        }

        // ESC -> Close Employee Modal

        if (

            event.key === "Escape" &&

            employeeModal

        ) {

            try {

                employeeModal.hide();

            }

            catch (error) {

                console.error(error);

            }

        }

        // Ctrl + P -> Print Dashboard

        if (

            event.ctrlKey &&

            event.key.toLowerCase() === "p"

        ) {

            event.preventDefault();

            printDashboard();

        }

        // F5 -> Refresh Dashboard

        if (

            event.key === "F5"

        ) {

            event.preventDefault();

            refreshDashboard();

        }

    }

);

// =====================================================
// Refresh Dashboard
// =====================================================

function refreshDashboard() {

    location.reload();

}

// =====================================================
// Export Employee Table
// =====================================================

function exportEmployeeTable() {

    alert(

        "Please use the Download Excel button to export the report."

    );

}

// =====================================================
// Print Dashboard
// =====================================================

function printDashboard() {

    window.print();

}
// =====================================================
// Cleanup
// =====================================================

window.addEventListener(

    "beforeunload",

    function () {

        try {

            if (employeeModal) {

                employeeModal.hide();

            }

        }

        catch (error) {

            console.error(error);

        }

        employeeModal = null;

        hrReportText = "";

        console.log("Dashboard Cleanup Completed.");

    }

);

// =====================================================
// Window Error Handler
// =====================================================

window.addEventListener(

    "error",

    function (event) {

        console.error(

            "Dashboard Error:",

            event.message,

            "\nFile:",

            event.filename,

            "\nLine:",

            event.lineno

        );

    }

);

// =====================================================
// Unhandled Promise Rejection
// =====================================================

window.addEventListener(

    "unhandledrejection",

    function (event) {

        console.error(

            "Unhandled Promise:",

            event.reason

        );

    }

);

// =====================================================
// Dashboard Ready
// =====================================================

console.log("==================================================");

console.log("Attendance Notification System Pro");

console.log("Dashboard JavaScript Initialized Successfully");

console.log("Version : 10.0 Enterprise");

console.log("Developed by Maharajan");

console.log("==================================================");