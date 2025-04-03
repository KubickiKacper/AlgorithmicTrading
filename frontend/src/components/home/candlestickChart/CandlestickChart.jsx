import "./CandlestickChart.css"
import Chart from "react-apexcharts"
import {apiUrl, CHART_OPTIONS} from "@utils/consts"
import useData from "@hooks/useData"

function CandlestickChart({requestData}) {
  const ENDPOINT = "/market/"
  const {data: chartData, loading, error} = useData(apiUrl + ENDPOINT, requestData)

  const candlestickData = chartData?.series?.[0]?.data || []

  const lineKeys = candlestickData.length > 0
    ? Object.keys(candlestickData[0]).filter(key => key.endsWith('_line_value'))
    : []

  const lineSeries = lineKeys.map((key) => {
    const lineName = key.replace('_line_value', '').toUpperCase()
    return {
      name: lineName,
      type: "line",
      data: candlestickData.map(item => ({
        x: new Date(item.x),
        y: item[key],
      })),
    }
  })

  const series = chartData?.series ? [...chartData.series] : []
  if (lineSeries.length > 0) {
    series.unshift(...lineSeries)
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

  const seriesColors = series.map(s => {
    console.log(s.type)
    if (s.type === "line") {
      if (s.name === "SHORT MA") return '#3399ff'
      if (s.name === "LONG MA") return '#00e396'
      return '#3399ff'
    }
  })

  const chartOptions = {
    ...CHART_OPTIONS,
    annotations: {xaxis: annotations},
    stroke: {
      ...CHART_OPTIONS.stroke,
      curve: 'straight',
      width: series.map(s => (s.type === "line" ? 2 : 1)),
      colors: seriesColors,
    },
    fill: {
      ...CHART_OPTIONS.fill,
      opacity: series.map(s => (s.type === "line" ? 1 : 0.8)),
    }
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
