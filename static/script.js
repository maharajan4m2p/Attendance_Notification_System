/*=========================================================
 Attendance Notification System
 Developed by Maharajan
=========================================================*/

document.addEventListener("DOMContentLoaded", function () {

    //------------------------------------------------------
    // Glass Card 3D Effect
    //------------------------------------------------------

    const card = document.querySelector(".glass-card");

    if (card) {

        document.addEventListener("mousemove", (e) => {

            const x =
                (window.innerWidth / 2 - e.pageX) / 40;

            const y =
                (window.innerHeight / 2 - e.pageY) / 40;

            card.style.transform =
                `rotateY(${x}deg) rotateX(${-y}deg)`;

        });

        document.addEventListener("mouseleave", () => {

            card.style.transform =
                "rotateX(0deg) rotateY(0deg)";

        });

    }

    //------------------------------------------------------
    // Upload Box
    //------------------------------------------------------

    const uploadBox =
        document.querySelector(".upload-box");

    const input =
        document.querySelector(
            "input[type=file]"
        );

    if (uploadBox && input) {

        input.addEventListener("change", function () {

            if (this.files.length > 0) {

                uploadBox.querySelector("h4").innerHTML =
                    this.files[0].name;

                uploadBox.style.borderColor =
                    "#22c55e";

                uploadBox.style.boxShadow =
                    "0 0 35px #22c55e";

            }

        });

    }

    //------------------------------------------------------
    // Button Animation
    //------------------------------------------------------

    const button =
        document.querySelector(".btn-analyze");

    if (button) {

        button.addEventListener("click", function () {

            this.innerHTML =
                "<i class='fa-solid fa-spinner fa-spin'></i> Processing...";

        });

    }

});


//----------------------------------------------------------
// Particles Background
//----------------------------------------------------------

particlesJS("particles-js", {

    particles: {

        number: {

            value: 80

        },

        color: {

            value: "#38bdf8"

        },

        shape: {

            type: "circle"

        },

        opacity: {

            value: 0.4

        },

        size: {

            value: 4

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