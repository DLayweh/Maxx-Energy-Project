async function fetchMockData() {
    try {
        const response = await fetch("https://maxx-energy-project.onrender.com/mock-public-data");
        if (!response.ok) throw new Error("Network response was not ok");
        
        const data = await response.json();
        console.log("Fetched Data:", data);  // Debugging log
        displayData(data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function displayData(data) {
    const tableBody = document.getElementById("data-table-body");
    tableBody.innerHTML = ""; // Clear previous entries

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
