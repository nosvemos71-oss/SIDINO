
document.addEventListener("DOMContentLoaded", function () {

    const STORAGE_KEY = "sidino_settings";

    const defaults = {
        color: "#2563eb",
        theme: "light",
        density: "normal",
        notifications: true
    };

    let settings = {
        ...defaults,
        ...JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}")
    };

    const root = document.documentElement;
    const body = document.body;

    function saveSettings() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    }

    function applySettings() {
        root.style.setProperty("--sidino-primary", settings.color);

        body.classList.toggle("settings-dark", settings.theme === "dark");
        body.classList.toggle("settings-compact", settings.density === "compact");

        document.querySelectorAll(".color-option").forEach(button => {
            button.classList.toggle(
                "selected",
                button.dataset.color === settings.color
            );
        });

        document.querySelectorAll(".theme-option").forEach(button => {
            button.classList.toggle(
                "selected",
                button.dataset.theme === settings.theme
            );
        });

        document.querySelectorAll(".density-option").forEach(button => {
            button.classList.toggle(
                "selected",
                button.dataset.density === settings.density
            );
        });

        const notifications = document.getElementById("notificationsToggle");

        if (notifications) {
            notifications.checked = settings.notifications;
        }
    }

    function showMessage(message) {
        const element = document.getElementById("settingsMessage");

        if (!element) return;

        element.textContent = message;

        setTimeout(() => {
            element.textContent = "";
        }, 2500);
    }

    // COLORES
    document.querySelectorAll(".color-option").forEach(button => {
        button.addEventListener("click", function () {
            settings.color = button.dataset.color;
            saveSettings();
            applySettings();
            showMessage("Color actualizado correctamente.");
        });
    });

    // TEMA
    document.querySelectorAll(".theme-option").forEach(button => {
        button.addEventListener("click", function () {
            settings.theme = button.dataset.theme;
            saveSettings();
            applySettings();
            showMessage("Tema actualizado.");
        });
    });

    // DENSIDAD
    document.querySelectorAll(".density-option").forEach(button => {
        button.addEventListener("click", function () {
            settings.density = button.dataset.density;
            saveSettings();
            applySettings();
            showMessage("Visualización actualizada.");
        });
    });

    // NOTIFICACIONES
    const notifications = document.getElementById("notificationsToggle");

    if (notifications) {
        notifications.addEventListener("change", function () {
            settings.notifications = notifications.checked;
            saveSettings();
            showMessage("Preferencias de notificación guardadas.");
        });
    }

    // RESTABLECER
    const resetButton = document.getElementById("resetSettings");

    if (resetButton) {
        resetButton.addEventListener("click", function () {
            settings = { ...defaults };
            saveSettings();
            applySettings();
            showMessage("Configuración restablecida.");
        });
    }

    // APLICAR PREFERENCIAS GUARDADAS
    applySettings();

});
