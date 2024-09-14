document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refresh-button');
    const sortPnlAscButton = document.getElementById('sort-pnl-asc');
    const sortPnlDescButton = document.getElementById('sort-pnl-desc');
    const sortSizeAscButton = document.getElementById('sort-size-asc');
    const sortSizeDescButton = document.getElementById('sort-size-desc');
    const sortRoeAscButton = document.getElementById('sort-roe-asc');
    const sortRoeDescButton = document.getElementById('sort-roe-desc');
    const positionsContainer = document.getElementById('positions-container');
    const totalPositionSizeElement = document.getElementById('total-position-size');
    let positionsData = [];

    function fetchData() {
        fetch('/crypto_dashboard/api/positions/')
            .then(response => response.json())
            .then(data => {
                positionsData = data.positions;
                totalPositionSizeElement.textContent = data.total_position_size.toFixed(2);
                displayData(positionsData);
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
                    <h5 class="card-title">${pos.pair}</h5>
                    <div class="row">
                        <div class="col-md-6">
                            <p class="card-text"><strong>Position Size:</strong> ${pos.active_pos} (${usdtSize.toFixed(2)} USDT)</p>
                            <p class="card-text ${pnlClass}"><strong>PnL:</strong> ${pnl.toFixed(2)}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="card-text"><strong>ROE:</strong> ${roe.toFixed(2)}%</p>
                            <p class="card-text"><strong>Locked Margin:</strong> ${pos.locked_margin.toFixed(2)}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="card-text"><strong>Current Price:</strong> ${pos.mark_price.toFixed(2)}</p>
                            <p class="card-text"><strong>Buy Price:</strong> ${pos.avg_price.toFixed(2)}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="card-text"><strong>Leverage:</strong> ${pos.leverage}</p>
                            <p class="card-text"><strong>Liquidation Price:</strong> ${pos.liquidation_price.toFixed(2)}</p>
                        </div>
                    </div>
                </div>
            </div>
            `;
            positionsContainer.appendChild(positionElement);
        });
    }

    function sortByPnlAsc() {
        const sortedData = positionsData.slice().sort((a, b) => a.pnl - b.pnl);
        displayData(sortedData);
    }

    function sortByPnlDesc() {
        const sortedData = positionsData.slice().sort((a, b) => b.pnl - a.pnl);
        displayData(sortedData);
    }

    function sortBySizeAsc() {
        const sortedData = positionsData.slice().sort((a, b) => (a.active_pos * a.mark_price) - (b.active_pos * b.mark_price));
        displayData(sortedData);
    }

    function sortBySizeDesc() {
        const sortedData = positionsData.slice().sort((a, b) => (b.active_pos * b.mark_price) - (a.active_pos * a.mark_price));
        displayData(sortedData);
    }

    function sortByRoeAsc() {
        const sortedData = positionsData.slice().sort((a, b) => a.roe - b.roe);
        displayData(sortedData);
    }

    function sortByRoeDesc() {
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

    fetchData();
});
