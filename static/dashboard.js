/*
=========================================================
Attendance Notification System Pro
Dashboard JavaScript
Version : 8.0 Enterprise (Ultra Performance)
Developed by Maharajan
=========================================================
*/

"use strict";

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

){

    document.getElementById("mEmpId").textContent = id;

    document.getElementById("mName").textContent = name;

    document.getElementById("mDepartment").textContent = department;

    document.getElementById("mDesignation").textContent = designation;

    document.getElementById("mDate").textContent = date;

    document.getElementById("mPunchIn").textContent = punchIn;

    document.getElementById("mPunchOut").textContent = punchOut;

    document.getElementById("mDailyOT").textContent = dailyOT || "00:00";

    document.getElementById("mMonthlyOT").textContent = monthlyOT || "00:00";

    document.getElementById("mRemainingOT").textContent = remainingOT || "00:00";

    document.getElementById("mDailyStatus").textContent = dailyStatus || "Normal";

    document.getElementById("mMonthlyStatus").textContent = monthlyStatus || "Normal";

    document.getElementById("mNotification").value = notification || "";

    // -----------------------------------------
    // Daily Status Badge
    // -----------------------------------------

    const daily = document.getElementById("mDailyStatus");

    daily.className = "badge";

    if(dailyStatus === "Normal"){

        daily.classList.add("bg-success");

    }

    else if(dailyStatus === "Warning"){

        daily.classList.add("bg-warning","text-dark");

    }

    else if(dailyStatus === "Limit Reached"){

        daily.classList.add("bg-dark");

    }

    else{

        daily.classList.add("bg-danger");

    }

    // -----------------------------------------
    // Monthly Status Badge
    // -----------------------------------------

    const monthly = document.getElementById("mMonthlyStatus");

    monthly.className = "badge";

    if(monthlyStatus === "Normal"){

        monthly.classList.add("bg-success");

    }

    else if(monthlyStatus === "Warning"){

        monthly.classList.add("bg-warning","text-dark");

    }

    else if(monthlyStatus === "Limit Reached"){

        monthly.classList.add("bg-dark");

    }

    else{

        monthly.classList.add("bg-danger");

    }

    employeeModal = new bootstrap.Modal(

        document.getElementById("employeeModal")

    );

    employeeModal.show();

}
// =====================================================
// Copy Employee Notification
// =====================================================

function copyNotification(){

    const notification = document.getElementById("mNotification");

    if(!notification){

        return;

    }

    navigator.clipboard.writeText(

        notification.value

    );

    alert("Notification copied successfully.");

}

// =====================================================
// Add Employee Notification to HR Report
// =====================================================

function addToReport(){

    const notification = document.getElementById(

        "mNotification"

    );

    const hrReport = document.getElementById(

        "hrReport"

    );

    if(

        !notification ||

        !hrReport

    ){

        return;

    }

    if(hrReportText.length > 0){

        hrReportText +=

        "\n\n========================================\n\n";

    }

    hrReportText += notification.value;

    hrReport.value = hrReportText;

    alert(

        "Employee added to HR Report."

    );

}

// =====================================================
// Copy HR Report
// =====================================================

function copyHRReport(){

    const report = document.getElementById(

        "hrReport"

    );

    if(!report){

        return;

    }

    navigator.clipboard.writeText(

        report.value

    );

    alert(

        "HR Report copied successfully."

    );

}

// =====================================================
// Send HR Report to WhatsApp
// =====================================================

function sendHRReport(){

    const report = document.getElementById(

        "hrReport"

    );

    if(!report){

        return;

    }

    window.open(

        "https://wa.me/?text=" +

        encodeURIComponent(

            report.value

        ),

        "_blank"

    );

}

// =====================================================
// Copy Late Punch Report
// =====================================================

function copyLatePunchReport(){

    const report = document.getElementById(

        "latePunchReport"

    );

    if(!report){

        return;

    }

    navigator.clipboard.writeText(

        report.value

    );

    alert(

        "Late / Missing Punch Report copied."

    );

}

// =====================================================
// Send Late Punch Report
// =====================================================

function sendLatePunchReport(){

    const report = document.getElementById(

        "latePunchReport"

    );

    if(!report){

        return;

    }

    window.open(

        "https://wa.me/?text=" +

        encodeURIComponent(

            report.value

        ),

        "_blank"

    );

}
// =====================================================
// Employee Search
// =====================================================

const employeeSearch = document.getElementById(

    "employeeSearch"

);

if(employeeSearch){

    employeeSearch.addEventListener(

        "keyup",

        function(){

            const keyword = this.value

                .toLowerCase()

                .trim();

            const rows = document.querySelectorAll(

                "#employeeTable tbody tr"

            );

            rows.forEach(function(row){

                const text = row.innerText.toLowerCase();

                row.style.display =

                    text.includes(keyword)

                    ? ""

                    : "none";

            });

        }

    );

}

// =====================================================
// Employee Filters
// =====================================================

const filterButtons = document.querySelectorAll(

    ".filter-btn"

);

filterButtons.forEach(function(button){

    button.addEventListener(

        "click",

        function(){

            // Remove Active Button

            filterButtons.forEach(function(btn){

                btn.classList.remove(

                    "active"

                );

            });

            this.classList.add(

                "active"

            );

            const filter = this.dataset.filter;

            const rows = document.querySelectorAll(

                "#employeeTable tbody tr"

            );

            rows.forEach(function(row){

                if(filter === "All"){

                    row.style.display = "";

                    return;

                }

                const text = row.innerText.toLowerCase();

                row.style.display =

                    text.includes(

                        filter.toLowerCase()

                    )

                    ? ""

                    : "none";

            });

        }

    );

});

// =====================================================
// Reset Search
// =====================================================

function clearSearch(){

    if(!employeeSearch){

        return;

    }

    employeeSearch.value = "";

    document.querySelectorAll(

        "#employeeTable tbody tr"

    ).forEach(function(row){

        row.style.display = "";

    });

}
// =====================================================
// Dashboard Charts
// =====================================================

window.addEventListener(

    "load",

    function(){

        const summary = window.dashboardData.summary || {};

        const employees = window.dashboardData.employees || [];

        // =============================================
        // Attendance Pie Chart
        // =============================================

        const attendanceCanvas = document.getElementById(

            "attendanceChart"

        );

        if(attendanceCanvas){

            new Chart(

                attendanceCanvas,

                {

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

                        plugins: {

                            legend: {

                                position: "bottom"

                            }

                        }

                    }

                }

            );

        }

        // =============================================
        // Attendance Statistics
        // =============================================

        const statisticsCanvas = document.getElementById(

            "statisticsChart"

        );

        if(statisticsCanvas){

            new Chart(

                statisticsCanvas,

                {

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

                            ]

                        }]

                    },

                    options: {

                        responsive: true,

                        plugins: {

                            legend: {

                                display: false

                            }

                        },

                        scales: {

                            y: {

                                beginAtZero: true

                            }

                        }

                    }

                }

            );

        }

        // =============================================
        // Monthly OT Status
        // =============================================

        const monthlyCanvas = document.getElementById(

            "monthlyOTChart"

        );

        if(monthlyCanvas){

            const warning = summary.warning || 0;

            const limit = summary.limit_reached || 0;

            const exceeded = summary.monthly_ot_exceeded || 0;

            const normal =

                (summary.total || 0)

                -

                warning

                -

                limit

                -

                exceeded;

            new Chart(

                monthlyCanvas,

                {

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

                        plugins: {

                            legend: {

                                position: "bottom"

                            }

                        }

                    }

                }

            );

        }

        // =============================================
        // Top Monthly OT Employees
        // =============================================

        const topCanvas = document.getElementById(

            "topOTChart"

        );

        if(topCanvas){

            const sorted = [...employees]

                .sort(

                    (a, b) =>

                    (b.monthly_ot_minutes || 0)

                    -

                    (a.monthly_ot_minutes || 0)

                )

                .slice(0, 10);

            new Chart(

                topCanvas,

                {

                    type: "bar",

                    data: {

                        labels: sorted.map(

                            emp => emp.name

                        ),

                        datasets: [{

                            label: "Monthly OT (Minutes)",

                            data: sorted.map(

                                emp => emp.monthly_ot_minutes || 0

                            )

                        }]

                    },

                    options: {

                        responsive: true,

                        indexAxis: "y",

                        scales: {

                            x: {

                                beginAtZero: true

                            }

                        }

                    }

                }

            );

        }

    }

);
// =====================================================
// Utility Functions
// =====================================================

// Escape HTML

function escapeHtml(text){

    if(text === null || text === undefined){

        return "";

    }

    return String(text)

        .replace(/&/g,"&amp;")

        .replace(/</g,"&lt;")

        .replace(/>/g,"&gt;")

        .replace(/"/g,"&quot;")

        .replace(/'/g,"&#039;");

}

// =====================================================
// Initialize Dashboard
// =====================================================

document.addEventListener(

    "DOMContentLoaded",

    function(){

        console.log("==========================================");

        console.log(

            "Attendance Notification System Pro"

        );

        console.log(

            "Dashboard Loaded Successfully"

        );

        console.log("==========================================");

        // Initialize HR Report Text

        const report = document.getElementById(

            "hrReport"

        );

        if(report){

            hrReportText = report.value || "";

        }

    }

);

// =====================================================
// Keyboard Shortcuts
// =====================================================

document.addEventListener(

    "keydown",

    function(event){

        // Ctrl + F -> Employee Search

        if(

            event.ctrlKey &&

            event.key.toLowerCase() === "f"

        ){

            event.preventDefault();

            const search = document.getElementById(

                "employeeSearch"

            );

            if(search){

                search.focus();

            }

        }

        // ESC -> Close Modal

        if(

            event.key === "Escape" &&

            employeeModal

        ){

            employeeModal.hide();

        }

    }

);

// =====================================================
// Refresh Dashboard
// =====================================================

function refreshDashboard(){

    location.reload();

}

// =====================================================
// Export Table (Future Support)
// =====================================================

function exportEmployeeTable(){

    alert(

        "Use the Download Excel button to export the report."

    );

}

// =====================================================
// Print Dashboard
// =====================================================

function printDashboard(){

    window.print();

}

// =====================================================
// Cleanup
// =====================================================

window.addEventListener(

    "beforeunload",

    function(){

        employeeModal = null;

        hrReportText = "";

    }

);

console.log(

    "Dashboard JavaScript Initialized Successfully."

);
