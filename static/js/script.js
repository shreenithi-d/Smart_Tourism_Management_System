 /* ==========================================
   SMART TOURISM MANAGEMENT SYSTEM
   Frontend JavaScript
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       Navbar Scroll Effect
    ========================== */

    const navbar = document.querySelector(".navbar");

    if (navbar) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 50) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        });
    }

    /* ==========================
       Destination Search
    ========================== */

    const searchInput = document.getElementById("destinationSearch");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const filter = this.value.toLowerCase();

            const cards = document.querySelectorAll(".destination-item");

            cards.forEach(card => {

                const text = card.textContent.toLowerCase();

                if (text.includes(filter)) {
                    card.style.display = "";
                } else {
                    card.style.display = "none";
                }

            });

        });

    }

    /* ==========================
       Counter Animation
    ========================== */

    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {

        const target = parseInt(counter.dataset.target || counter.innerText);
        let current = 0;

        const updateCounter = () => {

            const increment = Math.ceil(target / 80);

            if (current < target) {

                current += increment;

                if (current > target) {
                    current = target;
                }

                counter.innerText = current;

                setTimeout(updateCounter, 20);

            } else {

                counter.innerText = target;

            }

        };

        updateCounter();

    });

    /* ==========================
       Fade-Up Animation
    ========================== */

    const fadeElements = document.querySelectorAll(".fade-up");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }

        });

    }, {
        threshold: 0.2
    });

    fadeElements.forEach(element => {
        observer.observe(element);
    });

    /* ==========================
       Smooth Scroll
    ========================== */

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                e.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth"
                });

            }

        });

    });

    /* ==========================
       Auto Dismiss Alerts
    ========================== */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        setTimeout(() => {

            alert.classList.add("fade");

            setTimeout(() => {
                alert.remove();
            }, 500);

        }, 5000);

    });

    /* ==========================
       Hover Lift Effect
    ========================== */

    const hoverCards = document.querySelectorAll(
        ".destination-card, .favorite-card, .analytics-box, .stat-card"
    );

    hoverCards.forEach(card => {

        card.addEventListener("mouseenter", () => {
            card.style.transition = "0.3s ease";
        });

    });

    /* ==========================
       Button Loading State
    ========================== */

    const forms = document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener("submit", () => {

            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {

                submitButton.disabled = true;

                const originalText = submitButton.innerHTML;

                submitButton.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                }, 5000);

            }

        });

    });

    /* ==========================
       Destination Image Preview
    ========================== */

    const imageInput = document.querySelector(
        'input[name="image_url"]'
    );

    if (imageInput) {

        imageInput.addEventListener("blur", function () {

            const existingPreview =
                document.getElementById("imagePreview");

            if (existingPreview) {
                existingPreview.remove();
            }

            if (this.value.trim() !== "") {

                const img = document.createElement("img");

                img.src = this.value;
                img.id = "imagePreview";
                img.className = "img-fluid rounded mt-3 shadow";
                img.style.maxHeight = "250px";

                this.parentElement.appendChild(img);

            }

        });

    }

    /* ==========================
       Welcome Toast Message
    ========================== */

    const dashboard = document.querySelector(
        ".dashboard-card"
    );

    if (dashboard) {

        console.log(
            "Smart Tourism Management System Loaded Successfully"
        );

    }

});