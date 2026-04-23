const API_URL = "http://127.0.0.1:8000";
let allAssets = [];

async function loadAssets() {
    try {
        const response = await fetch(`${API_URL}/assets`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        allAssets = await response.json();
        displayAssets(allAssets);
    } catch (error) {
        console.error("Failed to load assets:", error);
        document.getElementById("asset-list").innerHTML =
            `<p class="empty-message">Failed to load assets.</p>`;
    }
}

function displayAssets(assets) {
    const container = document.getElementById("asset-list");
    container.innerHTML = "";

    if (assets.length === 0) {
        container.innerHTML = `<p class="empty-message">No assets found.</p>`;
        return;
    }

    assets.forEach(asset => {
        const div = document.createElement("div");
        div.classList.add("asset", asset.criticality);

        div.innerHTML = `
            <h3>${asset.name}</h3>
            <p><strong>Type:</strong> ${asset.asset_type}</p>
            <p><strong>Owner:</strong> ${asset.owner}</p>
            <p><strong>Criticality:</strong> ${asset.criticality}</p>
            <div class="extra-info"></div>
        `;

        // 🔥 Klick Event
        div.addEventListener("click", async () => {
            const extra = div.querySelector(".extra-info");

            // wenn schon geladen → schließen
            if (extra.innerHTML !== "") {
                extra.innerHTML = "";
                return;
            }

            try {
                const response = await fetch(`${API_URL}/assets/${asset.id}/risk`);
                const data = await response.json();

                extra.innerHTML = `
                    <hr>
                    <p><strong>Risk Score:</strong> ${data.risk_score}</p>
                    <p><strong>Dependencies:</strong> ${data.dependencies}</p>
                `;
            } catch (err) {
                extra.innerHTML = `<p style="color:red;">Error loading risk</p>`;
            }
        });

        container.appendChild(div);
    });
}

function setupSearch() {
    const searchInput = document.getElementById("search");

    searchInput.addEventListener("input", (event) => {
        const value = event.target.value.toLowerCase().trim();

        const filteredAssets = allAssets.filter(asset =>
            asset.name.toLowerCase().includes(value)
        );

        displayAssets(filteredAssets);
    });
}

loadAssets();
setupSearch();