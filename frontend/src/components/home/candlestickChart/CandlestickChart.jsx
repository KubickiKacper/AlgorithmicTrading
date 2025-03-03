import "./CandlestickChart.css"
import Chart from "react-apexcharts"
import {apiUrl, CHART_OPTIONS} from "@utils/consts"
import useData from "@hooks/useData"

function CandlestickChart() {
  const ENDPOINT = '/market/'
  const options = CHART_OPTIONS;

  const requestData = {
    ticker: "BTC-USD",
    start_date: "2019-02-01",
    end_date: "2025-03-02",
    interval: "1wk"
  };

  const {data: chartData, loading, error} = useData(apiUrl + ENDPOINT, requestData);

  return (
    <div className="chart-container">
      {loading && (
        <div className="chart-info">
          <div className="loading-spinner"></div>
          <div className="loading-text">Ładowanie...</div>
        </div>
      )}
      {
        error && (
          <div className="chart-info">
            <div className="error-text">Błąd: {error.message}</div>
          </div>
        )
      }

      {
        !loading && !error && chartData?.series && (
          <Chart options={options} series={chartData.series} type="candlestick" height={350}/>
        )
      }
    </div>
  )
}

export default CandlestickChart;
