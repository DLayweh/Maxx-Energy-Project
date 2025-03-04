async function fetchMockData() {
    try {
        const response = await fetch("https://maxx-energy-project.onrender.com/mock-public-data");
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function displayData(data) {
    const tableBody = document.getElementById("data-table-body");
    tableBody.innerHTML = "";

    data.forEach((item) => {
        const row = `
            <tr>
                <td>${item.id}</td>
                <td>${item.plant_name}</td>
                <td>${item.location}</td>
                <td>${item.energy_generated_kWh} kWh</td>
                <td>${item.timestamp}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Run function when page loads
window.onload = fetchMockData;
