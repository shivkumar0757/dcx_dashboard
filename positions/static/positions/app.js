document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refresh-button');
    const sortPnlAscButton = document.getElementById('sort-pnl-asc');
    const sortPnlDescButton = document.getElementById('sort-pnl-desc');
    const sortSizeAscButton = document.getElementById('sort-size-asc');
    const sortSizeDescButton = document.getElementById('sort-size-desc');
    const positionsContainer = document.getElementById('positions-container');
    const totalPositionSizeElement = document.getElementById('total-position-size');
    let positionsData = [];

    function fetchData() {
        fetch('/api/positions/')
            .then(response => response.json())
            .then(data => {
                // Ensure positionsData is set correctly to the array of positions
                positionsData = data.positions;
                totalPositionSizeElement.textContent = data.total_position_size.toFixed(2);
                displayData(positionsData);
            })
            .catch(error => console.error('Error fetching positions:', error));
    }

    function displayData(data) {
        positionsContainer.innerHTML = '';
        data.forEach(pos => {
            const pnl = (pos.mark_price - pos.avg_price) * pos.active_pos;
            const pnlClass = pnl >= 0 ? 'positive-pnl' : 'negative-pnl';
            const usdtSize = pos.active_pos * pos.mark_price;
            const positionElement = document.createElement('div');
            positionElement.innerHTML = `
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">${pos.pair}</h5>
                        <p class="card-text"><strong>Position Size:</strong> ${pos.active_pos} (${usdtSize.toFixed(2)} USDT)</p>
                        <p class="card-text ${pnlClass}"><strong>PnL:</strong> ${pnl.toFixed(2)}</p>
                    </div>
                </div>
            `;
            positionsContainer.appendChild(positionElement);
        });
    }

    function sortByPnlAsc() {
        const sortedData = positionsData.slice().sort((a, b) => {
            const pnlA = (a.mark_price - a.avg_price) * a.active_pos;
            const pnlB = (b.mark_price - b.avg_price) * b.active_pos;
            return pnlA - pnlB;
        });
        displayData(sortedData);
    }

    function sortByPnlDesc() {
        const sortedData = positionsData.slice().sort((a, b) => {
            const pnlA = (a.mark_price - a.avg_price) * a.active_pos;
            const pnlB = (b.mark_price - b.avg_price) * b.active_pos;
            return pnlB - pnlA;
        });
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

    refreshButton.addEventListener('click', fetchData);
    sortPnlAscButton.addEventListener('click', sortByPnlAsc);
    sortPnlDescButton.addEventListener('click', sortByPnlDesc);
    sortSizeAscButton.addEventListener('click', sortBySizeAsc);
    sortSizeDescButton.addEventListener('click', sortBySizeDesc);

    fetchData();
});
