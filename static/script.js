/*
=========================================================
Attendance Notification System Pro
JavaScript
Version : 5.0
Developed by Maharajan
=========================================================
*/

document.addEventListener("DOMContentLoaded", function () {

    //------------------------------------------------------
    // Glass Card Animation
    //------------------------------------------------------

    const card = document.querySelector(".glass-card");

    if (card) {

        document.addEventListener("mousemove", function (e) {

            const x =
                (window.innerWidth / 2 - e.pageX) / 40;

            const y =
                (window.innerHeight / 2 - e.pageY) / 40;

            card.style.transform =
                `rotateY(${x}deg) rotateX(${-y}deg)`;

        });

        document.addEventListener("mouseleave", function () {

            card.style.transform =
                "rotateX(0deg) rotateY(0deg)";

        });

    }

    //------------------------------------------------------
    // Upload File Name
    //------------------------------------------------------

    const uploadInput =
        document.querySelector("input[type='file']");

    if (uploadInput) {

        uploadInput.addEventListener("change", function () {

            if (this.files.length > 0) {

                console.log("Selected File : " + this.files[0].name);

                const uploadBox =
                    document.querySelector(".upload-box h4");

                if (uploadBox) {

                    uploadBox.innerHTML =
                        this.files[0].name;

                }

            }

        });

    }

    //------------------------------------------------------
    // Analyze Button
    //------------------------------------------------------

    const analyzeButton =
        document.querySelector(".btn-analyze");

    if (analyzeButton) {

        analyzeButton.addEventListener("click", function () {

            this.disabled = true;

            this.innerHTML =
                "<i class='fa-solid fa-spinner fa-spin'></i> Processing Attendance...";

        });

    }

});


//------------------------------------------------------
// Particles Background
//------------------------------------------------------

if (typeof particlesJS !== "undefined") {

    particlesJS("particles-js", {

        particles: {

            number: {

                value: 80

            },

            color: {

                value: "#0d6efd"

            },

            shape: {

                type: "circle"

            },

            opacity: {

                value: 0.5

            },

            size: {

                value: 3

            },

            move: {

                enable: true,

                speed: 2

            }

        },

        interactivity: {

            events: {

                onhover: {

                    enable: true,

                    mode: "repulse"

                }

            }

        }

    });

}