import "./CandlestickChart.css"
import Chart from "react-apexcharts"
import {CHART_OPTIONS} from "utils/consts"
import {useEffect, useState} from "react"
import axios from "axios";

function CandlestickChart() {
  const options = CHART_OPTIONS
  const [chartData, setChartData] = useState([])

  useEffect(() => {
    axios
      .post("http://localhost:5000/market/", {
        ticker: "BTC-USD",
        start_date: "2019-02-01",
        end_date: "2025-03-02",
        interval: "1wk"
      })
      .then(response => {
        console.log("Dane z API:", response.data);
        setChartData(response.data.series);
      })
      .catch(error => console.error("Błąd pobierania danych:", error));
  }, []);

  return (
    <div className="chart-container">
      <Chart options={options} series={chartData} type="candlestick" height={350}/>
    </div>
  );
}

export default CandlestickChart;
