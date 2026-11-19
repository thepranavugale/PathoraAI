
// document.addEventListener("DOMContentLoaded", () => {

//     const form = document.getElementById("careerForm");

//     if (form) {
//         form.addEventListener("submit", (event) => {

//             const inputs = form.querySelectorAll("input[type='number']");

//             for (const input of inputs) {
//                 const value = Number(input.value);

//                 if (!Number.isFinite(value) || value < 0 || value > 100) {
//                     event.preventDefault();
//                     alert("Please enter values between 0 and 100.");
//                     input.focus();
//                     return;
//                 }
//             }

//             const button = form.querySelector("button");

//             button.textContent = "Analyzing Your Career...";
//             button.disabled = true;
//         });
//     }

// });












document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // FORM VALIDATION
    // =========================

    const form = document.getElementById("careerForm");

    if (form) {

        form.addEventListener("submit", (event) => {

            const inputs = form.querySelectorAll(
                "input[type='number']"
            );

            for (const input of inputs) {

                const value = Number(input.value);

                if (
                    input.value.trim() === "" ||
                    !Number.isFinite(value) ||
                    value < 0 ||
                    value > 100
                ) {

                    event.preventDefault();

                    alert("Please enter a valid value between 0 and 100.");

                    input.focus();

                    return;
                }

            }

            const button = form.querySelector("button");

            if (button) {
                button.textContent = "Analyzing Your Career...";
                button.disabled = true;
            }

        });

    }


    // =========================
    // CAREER PROGRESS BARS
    // =========================

    const progressBars = document.querySelectorAll(".progress-fill");

    progressBars.forEach((bar) => {

        const score = Number(bar.dataset.score);

        if (Number.isFinite(score)) {

            const safeScore = Math.min(
                100,
                Math.max(0, score)
            );

            requestAnimationFrame(() => {

                bar.style.width = safeScore + "%";

            });

        }

    });


    // =========================
    // PAGE FADE-IN EFFECT
    // =========================

    document.body.classList.add("page-loaded");

});
