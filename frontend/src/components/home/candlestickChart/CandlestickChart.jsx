import "./CandlestickChart.css"
import Chart from "react-apexcharts"
import {apiUrl, CHART_OPTIONS} from "@utils/consts"
import useData from "@hooks/useData"

function CandlestickChart({requestData}) {
  const ENDPOINT = "/market/"
  const {data: chartData, loading, error} = useData(apiUrl + ENDPOINT, requestData)

  const lineSeriesData = chartData?.series?.[0]?.data
    ?.map(item => ({
      x: new Date(item.x),
      y: item.line_value,
    })) || []

  const series = chartData?.series ? [...chartData.series] : []

  if (lineSeriesData.length > 0) {
    series.unshift({
      name: "Line",
      type: "line",
      data: lineSeriesData,
    })
  }

  const annotations = chartData?.signals?.map(signal => {
    const color = signal.text === 'BUY' ? '#00E396' : '#FF4560'

    return {
      x: new Date(signal.x).getTime(),
      borderColor: color,
      label: {
        borderColor: color,
        style: {
          fontSize: '12px',
          color: '#fff',
          background: color
        },
        orientation: 'horizontal',
        text: signal.text,
      }
    }
  }) || []

  const chartOptions = {
    ...CHART_OPTIONS,
    annotations: {xaxis: annotations}
  }

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

      {!loading && !error && chartData?.series && (
        <Chart options={chartOptions} series={series} type="candlestick" height={350}/>
      )}
    </div>
  )
}


export default CandlestickChart
