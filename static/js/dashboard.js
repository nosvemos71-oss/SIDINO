/* ==========================================
   SIDINO - FUNCIONES GENERALES DEL PANEL
   ========================================== */

document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menuToggle");


    /* ======================================
       MENÚ LATERAL
    ====================================== */

    if (menuToggle) {

        menuToggle.addEventListener("click", function () {

            // En pantallas grandes
            if (window.innerWidth > 900) {

                document.body.classList.toggle("sidebar-collapsed");

            }

            // En celulares
            else {

                document.body.classList.toggle("mobile-sidebar-open");

            }

        });

    }


    /* ======================================
       CERRAR MENÚ EN CELULAR AL CAMBIAR PÁGINA
    ====================================== */

    document.querySelectorAll(".sidebar .nav-link").forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 900) {

                document.body.classList.remove("mobile-sidebar-open");

            }

        });

    });


    /* ======================================
       CERRAR MENÚ SI SE CAMBIA A PC
    ====================================== */

    window.addEventListener("resize", function () {

        if (window.innerWidth > 900) {

            document.body.classList.remove("mobile-sidebar-open");

        }

    });


    /* ======================================
       CAMBIO DE TEMA
    ====================================== */

    const themeSelector = document.getElementById("themeSelector");

    if (themeSelector) {

        themeSelector.addEventListener("change", function () {

            document.documentElement.setAttribute(
                "data-theme",
                this.value
            );

        });

    }

/* ==========================================
   PREFERENCIAS GLOBALES SIDINO
   Se aplican a todos los dashboards
========================================== */

(function () {
    const saved = JSON.parse(localStorage.getItem("sidino_settings") || "{}");

    const root = document.documentElement;
    const body = document.body;

    root.style.setProperty(
        "--sidino-primary",
        saved.color || "#2563eb"
    );

    body.classList.toggle("settings-dark", saved.theme === "dark");
    body.classList.toggle("settings-compact", saved.density === "compact");
})();

});