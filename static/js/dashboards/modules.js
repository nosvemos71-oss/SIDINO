
document.addEventListener("DOMContentLoaded", function () {
    const search = document.getElementById("moduleSearch");
    const table = document.getElementById("moduleTable");

    if (!search || !table) return;

    search.addEventListener("input", function () {
        const value = search.value.toLowerCase();
        const rows = table.querySelectorAll("tbody tr");

        rows.forEach(function (row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(value) ? "" : "none";
        });
    });
});
