document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refresh-button');
    const sortPnlAscButton = document.getElementById('sort-pnl-asc');
    const sortPnlDescButton = document.getElementById('sort-pnl-desc');
    const sortSizeAscButton = document.getElementById('sort-size-asc');
    const sortSizeDescButton = document.getElementById('sort-size-desc');
    const sortRoeAscButton = document.getElementById('sort-roe-asc');
    const sortRoeDescButton = document.getElementById('sort-roe-desc');
    const positionsContainer = document.getElementById('positions-container');
    // Account level
    const totalPositionSizeElement = document.getElementById('total-position-size');
    const totalLeverageElement = document.getElementById('total-leverage');
    const totalProfitElement = document.getElementById('total-profit-loss');
    const totalInvestment = document.getElementById('total-investment');
    const currentBalance = document.getElementById('current-balance');

    let currentSortingMode = null; // Track the selected sorting mode
    // Mode of positin INR, USDT, BOTH
    let selectedMode = "USDT"; // Default mode

    document.getElementById('mode-usdt').addEventListener('click', () => {
        selectedMode = "USDT";
        updateModeButtons();
        fetchData();
    });

    document.getElementById('mode-inr').addEventListener('click', () => {
        selectedMode = "INR";
        updateModeButtons();
        fetchData();
    });

    document.getElementById('mode-both').addEventListener('click', () => {
        selectedMode = "BOTH";
        updateModeButtons();
        fetchData();
    });

    function updateModeButtons() {
        document.getElementById('mode-usdt').classList.remove('active');
        document.getElementById('mode-inr').classList.remove('active');
        document.getElementById('mode-both').classList.remove('active');

        if (selectedMode === "USDT") {
            document.getElementById('mode-usdt').classList.add('active');
        } else if (selectedMode === "INR") {
            document.getElementById('mode-inr').classList.add('active');
        } else if (selectedMode === "BOTH") {
            document.getElementById('mode-both').classList.add('active');
        }
    }


    let positionsData = [];

    // fetch data based on margin mode
    function fetchData() {
        console.log("fetch event timestamp: ", new Date().toLocaleTimeString());
        const marginCurrency = selectedMode === "BOTH" ? ["USDT", "INR"] : [selectedMode];

        fetch(`/crypto_dashboard/api/positions/?margin_currency_short_name=${marginCurrency}`, {
            method: 'GET', // Changed to GET as we're using query parameters
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                positionsData = data.positions;
                totalPositionSizeElement.textContent = data.total_position_size.toFixed(6);
                totalLeverageElement.textContent = data.total_leverage.toFixed(2); //TODO make variable precision
                totalProfitElement.textContent = data.total_pnl.toFixed(6);
                totalInvestment.textContent = data.total_invested.toFixed(6);
                currentBalance.textContent = data.current_account_balance.toFixed(6);
                // Apply the current sorting mode if any
                if (currentSortingMode) {
                    applyCurrentSorting();
                } else {
                    displayData(positionsData); // Default display
                }
            })
            .catch(error => console.error('Error fetching positions:', error));
    }

    function displayData(data) {
        positionsContainer.innerHTML = '';
        data.forEach(pos => {
            const pnl = pos.pnl;
            const pnlClass = pnl >= 0 ? 'positive-pnl' : 'negative-pnl';
            const usdtSize = pos.active_pos * pos.mark_price;
            const roe = pos.roe;
            const positionElement = document.createElement('div');
            positionElement.innerHTML = `
                <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">${pos.pair}
                    <span class="badge rounded-pill  bg-secondary small px-2 py-1">${pos.margin_currency}</span></h5>
                    <div class="row">
                        <div class="col-md-6">
                            <p class="card-text"><strong>Position Size:</strong> ${pos.active_pos} (${usdtSize.toFixed(6)} USDT)</p>
                            <p class="card-text ${pnlClass}"><strong>PnL:</strong> ${pnl.toFixed(6)}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="card-text"><strong>ROE:</strong> ${roe.toFixed(6)}%</p>
                            <p class="card-text"><strong>Locked Margin:</strong> ${pos.locked_margin.toFixed(6)}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="card-text"><strong>Current Price:</strong> ${pos.mark_price.toFixed(6)}</p>
                            <p class="card-text"><strong>Buy Price:</strong> ${pos.avg_price.toFixed(6)}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="card-text"><strong>Leverage:</strong> ${pos.leverage}</p>
                            <p class="card-text"><strong>Liquidation Price:</strong> ${pos.liquidation_price.toFixed(6)}</p>
                        </div>
                    </div>
                </div>
            </div>
            `;
            positionsContainer.appendChild(positionElement);
        });
    }

    function applyCurrentSorting() {
        switch (currentSortingMode) {
            case 'sortPnlAsc':
                sortByPnlAsc();
                break;
            case 'sortPnlDesc':
                sortByPnlDesc();
                break;
            case 'sortSizeAsc':
                sortBySizeAsc();
                break;
            case 'sortSizeDesc':
                sortBySizeDesc();
                break;
            case 'sortRoeAsc':
                sortByRoeAsc();
                break;
            case 'sortRoeDesc':
                sortByRoeDesc();
                break;
            default:
                displayData(positionsData); // Default display
                break;
        }
    }

    function sortByPnlAsc() {
        currentSortingMode = 'sortPnlAsc';
        const sortedData = positionsData.slice().sort((a, b) => a.pnl - b.pnl);
        displayData(sortedData);
    }

    function sortByPnlDesc() {
        currentSortingMode = 'sortPnlDesc';
        const sortedData = positionsData.slice().sort((a, b) => b.pnl - a.pnl);
        displayData(sortedData);
    }

    function sortBySizeAsc() {
        currentSortingMode = 'sortSizeAsc';
        const sortedData = positionsData.slice().sort((a, b) => (a.active_pos * a.mark_price) - (b.active_pos * b.mark_price));
        displayData(sortedData);
    }

    function sortBySizeDesc() {
        currentSortingMode = 'sortSizeDesc';
        const sortedData = positionsData.slice().sort((a, b) => (b.active_pos * b.mark_price) - (a.active_pos * a.mark_price));
        displayData(sortedData);
    }

    function sortByRoeAsc() {
        currentSortingMode = 'sortRoeAsc';
        const sortedData = positionsData.slice().sort((a, b) => a.roe - b.roe);
        displayData(sortedData);
    }

    function sortByRoeDesc() {
        currentSortingMode = 'sortRoeDesc';
        const sortedData = positionsData.slice().sort((a, b) => b.roe - a.roe);
        displayData(sortedData);
    }

    refreshButton.addEventListener('click', fetchData);
    sortPnlAscButton.addEventListener('click', sortByPnlAsc);
    sortPnlDescButton.addEventListener('click', sortByPnlDesc);
    sortSizeAscButton.addEventListener('click', sortBySizeAsc);
    sortSizeDescButton.addEventListener('click', sortBySizeDesc);
    sortRoeAscButton.addEventListener('click', sortByRoeAsc);
    sortRoeDescButton.addEventListener('click', sortByRoeDesc);

    /// Initial fetch on page load
    fetchData();

    // Set interval to refresh every 5 seconds
    setInterval(fetchData, 5000);


});
