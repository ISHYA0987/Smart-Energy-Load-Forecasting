// ======================================
// Elements
// ======================================

const searchInput = document.getElementById("searchInput");
const zoneFilter = document.getElementById("zoneFilter");

const tableViewBtn = document.getElementById("tableViewBtn");
const cardViewBtn = document.getElementById("cardViewBtn");

const tableView = document.getElementById("tableView");
const cardView = document.getElementById("cardView");

const tableRows = document.querySelectorAll("#forecastTable tr");
const cardItems = document.querySelectorAll(".forecast-card-item");

// ======================================
// Search + Filter
// ======================================

function filterForecast() {

    const search = searchInput.value.toLowerCase().trim();
    const zone = zoneFilter.value;

    // ---------- Table ----------

    tableRows.forEach(row => {

        const time = row.cells[0].innerText.toLowerCase();
        const rowZone = row.cells[2].innerText.trim();

        const matchSearch = time.includes(search);
        const matchZone = zone === "All" || rowZone === zone;

        row.style.display =
            (matchSearch && matchZone)
            ? ""
            : "none";

    });

    // ---------- Cards ----------

    cardItems.forEach(card => {

        const time = card.dataset.time.toLowerCase();
        const rowZone = card.dataset.zone;

        const matchSearch = time.includes(search);
        const matchZone = zone === "All" || rowZone === zone;

        card.style.display =
            (matchSearch && matchZone)
            ? ""
            : "none";

    });

}

searchInput.addEventListener("keyup", filterForecast);
zoneFilter.addEventListener("change", filterForecast);

// ======================================
// View Toggle
// ======================================

tableViewBtn.addEventListener("click", () => {

    tableView.style.display = "block";
    cardView.style.display = "none";

    tableViewBtn.classList.remove("btn-outline-primary");
    tableViewBtn.classList.add("btn-primary");

    cardViewBtn.classList.remove("btn-primary");
    cardViewBtn.classList.add("btn-outline-primary");

});

cardViewBtn.addEventListener("click", () => {

    tableView.style.display = "none";
    cardView.style.display = "flex";

    cardViewBtn.classList.remove("btn-outline-primary");
    cardViewBtn.classList.add("btn-primary");

    tableViewBtn.classList.remove("btn-primary");
    tableViewBtn.classList.add("btn-outline-primary");

});

// ======================================
// Initialize
// ======================================

filterForecast();