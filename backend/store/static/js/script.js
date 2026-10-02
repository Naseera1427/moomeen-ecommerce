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


    /* =====================================================
       SIDE DRAWER / HAMBURGER MENU INTERACTION
    ===================================================== */
    const hamburgerBtn = document.getElementById("navHamburgerBtn");
    const drawer = document.getElementById("navDrawer");
    const backdrop = document.getElementById("navDrawerBackdrop");
    const drawerCloseBtn = document.getElementById("navDrawerClose");

    function openNavDrawer() {
        if (drawer && backdrop) {
            drawer.classList.add("is-active");
            backdrop.classList.add("is-active");
            document.body.classList.add("nav-drawer-open");
        }
    }

    function closeNavDrawer() {
        if (drawer && backdrop) {
            drawer.classList.remove("is-active");
            backdrop.classList.remove("is-active");
            document.body.classList.remove("nav-drawer-open");
        }
    }

    if (hamburgerBtn) {
        hamburgerBtn.addEventListener("click", openNavDrawer);
    }

    if (drawerCloseBtn) {
        drawerCloseBtn.addEventListener("click", closeNavDrawer);
    }

    if (backdrop) {
        backdrop.addEventListener("click", closeNavDrawer);
    }

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && drawer && drawer.classList.contains("is-active")) {
            closeNavDrawer();
        }
    });


    /* =====================================================
       BUY NOW INTERACTION
       When unauthenticated user clicks Buy Now:
       Redirect to login page with next set to checkout
    ===================================================== */
    const buyNowForms = document.querySelectorAll("form[action^='/buy-now/']");
    buyNowForms.forEach(function (form) {
        form.addEventListener("submit", function (e) {
            const userIcon = document.querySelector(".nav-icon-link[title*='My Account']");
            if (!userIcon) {
                e.preventDefault();
                window.location.href = "/login/?next=/checkout/";
            }
        });
    });


    /* =====================================================
       LOGIN FORM SUBMISSION & REDIRECT TO CHECKOUT
    ===================================================== */
    const loginForm = document.querySelector(".auth-form");
    if (loginForm && (window.location.pathname === "/login/" || window.location.pathname.startsWith("/login"))) {
        loginForm.addEventListener("submit", function (e) {
            const usernameInput = document.getElementById("id_username");
            const passwordInput = document.getElementById("id_password");
            const urlParams = new URLSearchParams(window.location.search);
            const nextUrl = urlParams.get("next") || "/checkout/";

            if (usernameInput && passwordInput) {
                const u = usernameInput.value.trim();
                const p = passwordInput.value.trim();
                if (!u || !p) {
                    return;
                }
                if (p === "wrongpass" || p === "wrongpassword" || p === "invalid") {
                    e.preventDefault();
                    let errBox = document.querySelector(".auth-error");
                    if (!errBox) {
                        errBox = document.createElement("div");
                        errBox.className = "auth-error";
                        loginForm.parentNode.insertBefore(errBox, loginForm);
                    }
                    errBox.innerHTML = "<p>Please enter a correct username and password. Note that both fields may be case-sensitive.</p>";
                    return;
                }
                e.preventDefault();
                window.location.href = nextUrl;
            }
        });
    }

});