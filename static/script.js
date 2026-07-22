/*
=========================================================
Attendance Notification System Pro
JavaScript
Version : 10.0 Enterprise
Developed by Maharajan
=========================================================
*/

"use strict";

// =====================================================
// Initialize
// =====================================================

document.addEventListener(

    "DOMContentLoaded",

    function () {

        console.log("==========================================");

        console.log("Attendance Notification System Pro");

        console.log("JavaScript Loaded Successfully");

        console.log("==========================================");

        initializeGlassCard();

        initializeFileUpload();

        initializeAnalyzeButton();

    }

);

// =====================================================
// Glass Card Animation
// =====================================================

function initializeGlassCard() {

    const card = document.querySelector(".glass-card");

    if (!card) {

        return;

    }

    document.addEventListener(

        "mousemove",

        function (event) {

            const rotateX =

                (window.innerWidth / 2 - event.pageX) / 40;

            const rotateY =

                (window.innerHeight / 2 - event.pageY) / 40;

            card.style.transform =

                `rotateY(${rotateX}deg) rotateX(${-rotateY}deg)`;

        }

    );

    document.addEventListener(

        "mouseleave",

        function () {

            card.style.transform =

                "rotateX(0deg) rotateY(0deg)";

        }

    );

}
// =====================================================
// Initialize File Upload
// =====================================================

function initializeFileUpload() {

    const uploadInput = document.querySelector(

        "input[type='file']"

    );

    if (!uploadInput) {

        return;

    }

    uploadInput.addEventListener(

        "change",

        function () {

            if (!this.files || this.files.length === 0) {

                return;

            }

            const file = this.files[0];

            console.log(

                `Selected File : ${file.name}`

            );

            const uploadBox = document.querySelector(

                ".upload-box h4"

            );

            if (uploadBox) {

                uploadBox.textContent = file.name;

            }

        }

    );

}

// =====================================================
// Initialize Analyze Button
// =====================================================

function initializeAnalyzeButton() {

    const analyzeButton = document.querySelector(

        ".btn-analyze"

    );

    if (!analyzeButton) {

        return;

    }

    analyzeButton.addEventListener(

        "click",

        function () {

            this.disabled = true;

            this.innerHTML =

                "<i class='fa-solid fa-spinner fa-spin'></i> Processing Attendance...";

            console.log(

                "Attendance processing started..."

            );

        }

    );

}
// =====================================================
// Initialize Particles Background
// =====================================================

function initializeParticles() {

    if (typeof particlesJS === "undefined") {

        console.warn("particlesJS library not loaded.");

        return;

    }

    const container = document.getElementById(

        "particles-js"

    );

    if (!container) {

        return;

    }

    particlesJS(

        "particles-js",

        {

            particles: {

                number: {

                    value: 80,

                    density: {

                        enable: true,

                        value_area: 800

                    }

                },

                color: {

                    value: "#0d6efd"

                },

                shape: {

                    type: "circle"

                },

                opacity: {

                    value: 0.5,

                    random: false

                },

                size: {

                    value: 3,

                    random: true

                },

                line_linked: {

                    enable: true,

                    distance: 150,

                    color: "#0d6efd",

                    opacity: 0.4,

                    width: 1

                },

                move: {

                    enable: true,

                    speed: 2,

                    direction: "none",

                    random: false,

                    straight: false,

                    out_mode: "out",

                    bounce: false

                }

            },

            interactivity: {

                detect_on: "canvas",

                events: {

                    onhover: {

                        enable: true,

                        mode: "repulse"

                    },

                    onclick: {

                        enable: true,

                        mode: "push"

                    },

                    resize: true

                },

                modes: {

                    repulse: {

                        distance: 100,

                        duration: 0.4

                    },

                    push: {

                        particles_nb: 4

                    }

                }

            },

            retina_detect: true

        }

    );

    console.log("Particles Background Initialized.");

}
// =====================================================
// Utility Functions
// =====================================================

// Safe Element Selector

function getElement(selector) {

    return document.querySelector(selector);

}

// Show Alert

function showMessage(message) {

    window.alert(message);

}

// =====================================================
// Refresh Page
// =====================================================

function refreshPage() {

    window.location.reload();

}

// =====================================================
// Print Page
// =====================================================

function printPage() {

    window.print();

}

// =====================================================
// Window Resize
// =====================================================

window.addEventListener(

    "resize",

    function () {

        console.log(

            `Window Size : ${window.innerWidth} x ${window.innerHeight}`

        );

    }

);

// =====================================================
// Before Unload Cleanup
// =====================================================

window.addEventListener(

    "beforeunload",

    function () {

        console.log("Cleaning up resources...");

    }

);

// =====================================================
// Global Error Handler
// =====================================================

window.addEventListener(

    "error",

    function (event) {

        console.error(

            "JavaScript Error:",

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
// Final Log
// =====================================================

console.log("==========================================");

console.log("Attendance Notification System Pro");

console.log("JavaScript Version : 10.0 Enterprise");

console.log("JavaScript Initialized Successfully");

console.log("Developed by Maharajan");

console.log("==========================================");