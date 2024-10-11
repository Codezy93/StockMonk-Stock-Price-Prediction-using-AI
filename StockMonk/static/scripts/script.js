function getChartData(){
    console.log('Got a Request');
    const ticker = document.getElementById("StockTicker").value;
    console.log(ticker);
    const selectedOption = document.querySelector('input[name="selection"]:checked').value;
    const data = {
        ticker_id: ticker,
    };
    fetch('http://127.0.0.1:5000/api/get-stock-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify(data),
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        const trace = {
            x: data.x,
            open: data.open,
            high: data.high,
            low: data.low,
            close: data.close,
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
        };
        const layout = {
            title: `Candlestick Chart for ${data.ticker_id}`,
            xaxis: {
                title: 'Date',
                rangeslider: {
                    visible: false
                }
            },
            yaxis: {
                title: 'Stock Price'
            }
        };
        Plotly.newPlot('candlestickDiv', [trace], layout);
    });
}