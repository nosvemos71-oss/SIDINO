
document.addEventListener("DOMContentLoaded", function () {

    const table = document.getElementById("moduleTable");
    const search = document.getElementById("moduleSearch");
    const clearSearch = document.getElementById("clearSearch");

    const modal = document.getElementById("moduleModal");
    const viewModal = document.getElementById("viewModal");

    const form = document.getElementById("moduleForm");
    const openForm = document.getElementById("openModuleForm");
    const closeForm = document.getElementById("closeModuleForm");
    const cancelForm = document.getElementById("cancelModuleForm");

    const modalTitle = document.getElementById("modalTitle");
    const visibleRows = document.getElementById("visibleRows");
    const viewContent = document.getElementById("viewRecordContent");

    let editingRow = null;

    if (!table) return;

    const tbody = table.querySelector("tbody");

    function updateCount() {
        const rows = Array.from(tbody.querySelectorAll("tr"));
        const visible = rows.filter(row => row.style.display !== "none");

        if (visibleRows) {
            visibleRows.textContent =
                `Mostrando ${visible.length} registros`;
        }
    }

    function openModal(title) {
        modalTitle.textContent = title;
        modal.classList.add("show");
    }

    function closeModal() {
        modal.classList.remove("show");
        form.reset();
        editingRow = null;
    }

    function openViewModal() {
        viewModal.classList.add("show");
    }

    function closeViewModal() {
        viewModal.classList.remove("show");
    }

    // ABRIR FORMULARIO

    if (openForm) {
        openForm.addEventListener("click", function () {
            editingRow = null;
            form.reset();
            openModal("Nuevo registro");
        });
    }

    // CERRAR FORMULARIO

    if (closeForm) {
        closeForm.addEventListener("click", closeModal);
    }

    if (cancelForm) {
        cancelForm.addEventListener("click", closeModal);
    }

    // CERRAR MODAL AL HACER CLIC AFUERA

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    viewModal.addEventListener("click", function (event) {
        if (event.target === viewModal) {
            closeViewModal();
        }
    });

    document.querySelectorAll(".closeViewModal").forEach(button => {
        button.addEventListener("click", closeViewModal);
    });

    // BUSCADOR

    if (search) {
        search.addEventListener("input", function () {
            const value = search.value.toLowerCase().trim();

            tbody.querySelectorAll("tr").forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(value) ? "" : "none";
            });

            updateCount();
        });
    }

    // RESTABLECER BUSQUEDA

    if (clearSearch) {
        clearSearch.addEventListener("click", function () {
            search.value = "";

            tbody.querySelectorAll("tr").forEach(row => {
                row.style.display = "";
            });

            updateCount();
        });
    }

    // OBTENER CELDAS DE UNA FILA

    function getRowValues(row) {
        const cells = Array.from(row.querySelectorAll("td"));

        return cells.slice(0, -1).map(cell => cell.textContent.trim());
    }

    // BOTONES DE LAS FILAS

    function attachRowEvents(row) {

        const viewButton = row.querySelector(".view-action");
        const editButton = row.querySelector(".edit-action");
        const deleteButton = row.querySelector(".delete-action");

        // VER

        if (viewButton) {
            viewButton.onclick = function () {

                const values = getRowValues(row);
                const headers = Array.from(
                    table.querySelectorAll("thead th")
                ).slice(0, -1);

                viewContent.innerHTML = "";

                values.forEach((value, index) => {

                    const item = document.createElement("div");
                    item.className = "module-view-item";

                    const label = document.createElement("label");
                    label.textContent = headers[index]
                        ? headers[index].textContent
                        : `Dato ${index + 1}`;

                    const text = document.createElement("p");
                    text.textContent = value;

                    item.appendChild(label);
                    item.appendChild(text);

                    viewContent.appendChild(item);
                });

                openViewModal();
            };
        }

        // EDITAR

        if (editButton) {
            editButton.onclick = function () {

                editingRow = row;

                const values = getRowValues(row);
                const inputs = form.querySelectorAll("input");

                inputs.forEach((input, index) => {
                    input.value = values[index] || "";
                });

                openModal("Editar registro");
            };
        }

        // ELIMINAR

        if (deleteButton) {
            deleteButton.onclick = function () {

                const confirmDelete = confirm(
                    "¿Estás seguro de que deseas eliminar este registro de la vista?"
                );

                if (confirmDelete) {
                    row.remove();
                    updateCount();
                }
            };
        }
    }

    // ASIGNAR EVENTOS A LAS FILAS EXISTENTES

    tbody.querySelectorAll("tr").forEach(row => {
        if (row.querySelector(".row-action")) {
            attachRowEvents(row);
        }
    });

    // GUARDAR FORMULARIO DEMOSTRATIVO

    form.addEventListener("submit", function (event) {

        event.preventDefault();

        const values = Array.from(form.querySelectorAll("input"))
            .map(input => input.value.trim());

        if (values.some(value => value === "")) {
            alert("Por favor completa todos los campos.");
            return;
        }

        const totalColumns = table.querySelectorAll("thead th").length - 1;

        if (editingRow) {

            const cells = editingRow.querySelectorAll("td");

            values.forEach((value, index) => {
                if (cells[index]) {
                    cells[index].textContent = value;
                }
            });

            alert("Registro actualizado visualmente.");

        } else {

            const row = document.createElement("tr");

            for (let i = 0; i < totalColumns; i++) {
                const cell = document.createElement("td");
                cell.textContent = values[i] || "—";
                row.appendChild(cell);
            }

            const actions = document.createElement("td");

            actions.innerHTML = `
                <div class="module-row-actions">
                    <button class="row-action view-action" title="Visualizar">
                        <i class="fa-solid fa-eye"></i>
                    </button>

                    <button class="row-action edit-action" title="Editar">
                        <i class="fa-solid fa-pen"></i>
                    </button>

                    <button class="row-action delete-action" title="Eliminar">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            `;

            row.appendChild(actions);
            tbody.prepend(row);

            attachRowEvents(row);

            alert("Registro agregado a la vista de demostración.");
        }

        closeModal();
        updateCount();

    });

    updateCount();

});
