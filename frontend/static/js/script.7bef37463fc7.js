/* =========================================================
   MOOMEEN PRODUCTS
   Main JavaScript
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {


    /* =====================================================
       FAQ ACCORDION
    ===================================================== */

    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(function (question) {

        question.addEventListener("click", function () {

            const currentItem = this.closest(".faq-item");

            // Close other FAQ items
            document.querySelectorAll(".faq-item").forEach(function (item) {

                if (item !== currentItem) {
                    item.classList.remove("active");
                }

            });

            // Toggle current FAQ
            currentItem.classList.toggle("active");

        });

    });


    /* =====================================================
       IMAGE ERROR HANDLING
       If an image is missing, hide broken image display
    ===================================================== */

    const images = document.querySelectorAll("img");

    images.forEach(function (image) {

        image.addEventListener("error", function () {

            this.style.display = "none";

        });

    });


    /* =====================================================
       PRODUCT IMAGE HOVER
       Small smooth interaction
    ===================================================== */

    const productCards = document.querySelectorAll(".home-product-card");

    productCards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            this.classList.add("is-hovered");
        });

        card.addEventListener("mouseleave", function () {
            this.classList.remove("is-hovered");
        });

    });


    /* =====================================================
       CATEGORY CARD INTERACTION
    ===================================================== */

    const categoryCards = document.querySelectorAll(".category-card");

    categoryCards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            this.classList.add("is-hovered");
        });

        card.addEventListener("mouseleave", function () {
            this.classList.remove("is-hovered");
        });

    });


    /* =====================================================
       PREVENT DOUBLE CLICK ON BUTTONS
       Avoid accidental repeated clicks
    ===================================================== */

    const actionLinks = document.querySelectorAll(
        ".primary-btn, .checkout-btn"
    );

    actionLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            if (this.classList.contains("clicked")) {
                return;
            }

            this.classList.add("clicked");

        });

    });


    /* =====================================================
       SCROLL REVEAL
       Sections gently appear when entering viewport
    ===================================================== */

    const revealElements = document.querySelectorAll(
        ".category-card, .home-product-card, .ingredient-card, " +
        ".home-review-card, .about-content, .faq-item"
    );

    if ("IntersectionObserver" in window) {

        const observer = new IntersectionObserver(
            function (entries, observer) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.classList.add("visible");

                        observer.unobserve(entry.target);

                    }

                });

            },
            {
                threshold: 0.12
            }
        );

        revealElements.forEach(function (element) {
            observer.observe(element);
        });

    }


    /* =====================================================
       CURRENT YEAR
       Automatically update footer year if needed
    ===================================================== */

    const yearElement = document.querySelector("[data-current-year]");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

});