import "./CandlestickChart.css"
import Chart from "react-apexcharts"
import {apiUrl, CHART_OPTIONS} from "@utils/consts"
import useData from "@hooks/useData"

function CandlestickChart({requestData}) {
  const ENDPOINT = "/market/"
  const {data: chartData, loading, error} = useData(apiUrl + ENDPOINT, requestData)

  const lineSeries = {
    name: 'Line',
    type: 'line',
    data: chartData?.series?.[0]?.data?.map(item => ({
      x: new Date(item.x),
      y: item.y[3],
    })) || [],
  }

  const series = chartData?.series ? [
    lineSeries,
    ...chartData.series,
  ] : []

  return (
    <div className="chart-container">
      {loading && (
        <div className="chart-info">
          <div className="loading-spinner"></div>
          <div className="loading-text">Loading...</div>
        </div>
      )}

      {error && (
        <div className="chart-info">
          <div className="error-text">Error: {error.message}</div>
        </div>
      )}

      {
        !loading && !error && chartData?.series && (
          <Chart options={CHART_OPTIONS} series={series} type="candlestick" height={350}/>
        )
      }
    </div>
  )
}

export default CandlestickChart
