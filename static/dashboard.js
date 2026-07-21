/*
=========================================================
Attendance Notification System Pro
Dashboard JavaScript
Version : 5.0 Enterprise
Developed by Maharajan
=========================================================
*/

let hrReportText = "";

let employeeModal = null;
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

document.getElementById("mEmpId").innerHTML=id;

document.getElementById("mName").innerHTML=name;

document.getElementById("mDepartment").innerHTML=department;

document.getElementById("mDesignation").innerHTML=designation;

document.getElementById("mDate").innerHTML=date;

document.getElementById("mPunchIn").innerHTML=punchIn;

document.getElementById("mPunchOut").innerHTML=punchOut;

document.getElementById("mDailyOT").innerHTML=dailyOT;

document.getElementById("mMonthlyOT").innerHTML=monthlyOT;

document.getElementById("mRemainingOT").innerHTML=remainingOT;

document.getElementById("mDailyStatus").innerHTML=dailyStatus;

document.getElementById("mMonthlyStatus").innerHTML=monthlyStatus;

document.getElementById("mNotification").value=notification;

const daily=document.getElementById("mDailyStatus");

daily.className="badge";

if(dailyStatus==="Allowed"){

daily.classList.add("bg-success");

}

else if(dailyStatus==="Limit Reached"){

daily.classList.add("bg-warning","text-dark");

}

else{

daily.classList.add("bg-danger");

}

const monthly=document.getElementById("mMonthlyStatus");

monthly.className="badge";

if(monthlyStatus==="Normal"){

monthly.classList.add("bg-success");

}

else if(monthlyStatus==="Warning"){

monthly.classList.add("bg-warning","text-dark");

}

else if(monthlyStatus==="Limit Reached"){

monthly.classList.add("bg-dark");

}

else{

monthly.classList.add("bg-danger");

}

employeeModal=new bootstrap.Modal(

document.getElementById("employeeModal")

);

employeeModal.show();

}
function copyNotification(){

navigator.clipboard.writeText(

document.getElementById("mNotification").value

);

alert("Notification copied.");

}
function addToReport(){

const notification=

document.getElementById("mNotification").value;

hrReportText+=notification+"\n\n-------------------------\n\n";

document.getElementById("hrReport").value=hrReportText;

alert("Added to HR Report.");

}
// =====================================================
// Copy HR Report
// =====================================================

function copyHRReport(){

const report=document.getElementById("hrReport");

if(!report)return;

navigator.clipboard.writeText(report.value);

alert("HR Report copied successfully.");

}
// =====================================================
// Send HR Report
// =====================================================

function sendHRReport(){

const report=document.getElementById("hrReport");

if(!report)return;

window.open(

"https://wa.me/?text="+

encodeURIComponent(report.value),

"_blank"

);

}
// =====================================================
// Copy Late Punch Report
// =====================================================

function copyLatePunchReport(){

const report=document.getElementById("latePunchReport");

if(!report)return;

navigator.clipboard.writeText(report.value);

alert("Late Punch Report copied.");

}
// =====================================================
// Send Late Punch Report
// =====================================================

function sendLatePunchReport(){

const report=document.getElementById("latePunchReport");

if(!report)return;

window.open(

"https://wa.me/?text="+

encodeURIComponent(report.value),

"_blank"

);

}
// =====================================================
// Employee Search
// =====================================================

const employeeSearch=document.getElementById(

"employeeSearch"

);

if(employeeSearch){

employeeSearch.addEventListener(

"keyup",

function(){

const value=this.value.toLowerCase();

document.querySelectorAll(

"#employeeTable tbody tr"

).forEach(function(row){

row.style.display=

row.innerText.toLowerCase().includes(value)

?

""

:

"none";

});

}

);

}
// =====================================================
// Employee Filter
// =====================================================

document.querySelectorAll(

".filter-btn"

).forEach(function(button){

button.addEventListener(

"click",

function(){

const filter=this.dataset.filter;

document.querySelectorAll(

"#employeeTable tbody tr"

).forEach(function(row){

if(filter==="All"){

row.style.display="";

return;

}

row.style.display=

row.innerText.includes(filter)

?

""

:

"none";

});

}

);

});
// =====================================================
// Dashboard Charts
// =====================================================

window.addEventListener(

"load",

function(){

const summary=window.dashboardData.summary;

const employees=window.dashboardData.employees;


// =============================================
// Attendance Pie
// =============================================

new Chart(

document.getElementById("attendanceChart"),

{

type:"pie",

data:{

labels:[

"Present",

"Late",

"Early Out",

"Missing In",

"Missing Out"

],

datasets:[{

data:[

summary.present,

summary.late_in,

summary.early_out,

summary.missing_in,

summary.missing_out

],

backgroundColor:[

"#198754",

"#dc3545",

"#fd7e14",

"#6c757d",

"#212529"

]

}]

}

});


// =============================================
// Statistics
// =============================================

new Chart(

document.getElementById("statisticsChart"),

{

type:"bar",

data:{

labels:[

"Present",

"Late",

"Early",

"Daily OT"

],

datasets:[{

data:[

summary.present,

summary.late_in,

summary.early_out,

summary.overtime

]

}]

},

options:{

plugins:{

legend:{

display:false

}

}

}

});


// =============================================
// Monthly OT Status
// =============================================

new Chart(

document.getElementById("monthlyOTChart"),

{

type:"doughnut",

data:{

labels:[

"Normal",

"Warning",

"Limit Reached",

"Exceeded"

],

datasets:[{

data:[

summary.total-

summary.monthly_warning-

summary.monthly_limit_reached-

summary.monthly_ot_exceeded,

summary.monthly_warning,

summary.monthly_limit_reached,

summary.monthly_ot_exceeded

]

}]

}

});


// =============================================
// Top Monthly OT
// =============================================

const sorted=[...employees]

.sort(

(a,b)=>

b.monthly_ot_minutes-

a.monthly_ot_minutes

)

.slice(0,10);

new Chart(

document.getElementById("topOTChart"),

{

type:"bar",

data:{

labels:sorted.map(

e=>e.name

),

datasets:[{

label:"Monthly OT (Minutes)",

data:sorted.map(

e=>e.monthly_ot_minutes

)

}]

},

options:{

indexAxis:"y"

}

});

});