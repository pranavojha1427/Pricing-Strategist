document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('product-grid');
    const storeTitle = document.getElementById('store-title');
    const generateBtn = document.getElementById('generate-btn');
    const businessInput = document.getElementById('business-input');
    const urlInput = document.getElementById('url-input');
    const statusText = document.getElementById('status-text');
    const statusPulse = document.getElementById('status-pulse');
    const commandCenter = document.querySelector('.command-center');
    
    async function loadCurrentStore() {
        try {
            const response = await fetch('/src/data/store_data.json');
            if (response.ok) {
                const data = await response.json();
                renderStore(data, false); // Don't scroll on initial load
            }
        } catch (e) {
            console.log("No existing store data found.");
        }
    }

    async function handleGenerate() {
        const businessName = businessInput.value || "OmniStrike Store";
        const targetUrl = urlInput.value;

        if (!targetUrl) {
            alert("Please enter a competitor URL!");
            return;
        }

        // UI Loading State
        generateBtn.disabled = true;
        generateBtn.textContent = "🚀 Launching AI...";
        statusText.textContent = "Zynd AI is building your store...";
        statusPulse.className = "pulse loading"; 
        productGrid.style.opacity = "0.3";

        try {
            const response = await fetch('http://localhost:5000/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ business_name: businessName, target_url: targetUrl })
            });

            if (!response.ok) throw new Error("Generation failed");

            const data = await response.json();
            
            // Dramatic Transition
            statusText.textContent = "Store Generated Successfully!";
            statusPulse.className = "pulse success";
            
            setTimeout(() => {
                renderStore(data, true); // Scroll to results
                generateBtn.textContent = "Re-Generate Store";
                generateBtn.disabled = false;
            }, 500);

        } catch (error) {
            alert("Error in Pipeline: " + error.message);
            statusText.textContent = "Pipeline Failed";
            statusPulse.className = "pulse error";
            generateBtn.disabled = false;
            generateBtn.textContent = "Try Again";
        } finally {
            productGrid.style.opacity = "1";
        }
    }

    function renderStore(data, shouldScroll) {
        storeTitle.textContent = data.store_name;
        productGrid.innerHTML = '';
        
        data.items.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.style.animation = `fadeInUp 0.8s ease forwards ${index * 0.1}s`;
            
            card.innerHTML = `
                <img src="${item.image_url}" alt="${item.product_name}" class="product-image" onerror="this.src='https://placehold.co/400x300?text=AI+Image+Loading'">
                <h3 class="product-name">${item.product_name}</h3>
                <div class="price-container">
                    <div class="price-block">
                        <span class="original-price">₹${item.original_price}</span>
                        <span class="new-price">${item.new_price}</span>
                    </div>
                    <div class="discount-badge">${item.discount_applied}</div>
                </div>
            `;
            productGrid.appendChild(card);
        });

        if (shouldScroll) {
            productGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    generateBtn.addEventListener('click', handleGenerate);
    loadCurrentStore();
});
