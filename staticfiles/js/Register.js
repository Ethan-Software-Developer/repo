document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".form-step");
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    const submitBtn = document.getElementById("submitBtn");
    let currentStep = 0;

    function showStep(step) {
        steps.forEach((formStep, index) => {
            formStep.classList.toggle("active", index === step);
        });

        // Update button visibility
        prevBtn.disabled = step === 0;
        nextBtn.style.display = step === steps.length - 1 ? "none" : "inline-block";
        submitBtn.style.display = step === steps.length - 1 ? "inline-block" : "none";
    }

    nextBtn.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            showStep(currentStep);
        }
    });

    prevBtn.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    });

    // Initialize form
    showStep(currentStep);
});
