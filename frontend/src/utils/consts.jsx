export const apiUrl = 'http://localhost:5000/'

export const CHART_OPTIONS = {
  chart: {
    type: "candlestick",
    height: 350,
    animations: {
      enabled: false,
    },
    zoom: {
      enabled: true,
      type: 'x',
      autoScaleYaxis: true,
    }
  },
  xaxis: {
    type: "datetime",
    labels: {style: {colors: "#ccc"}}
  },
  yaxis: {
    tooltip: {enabled: true},
    labels: {
      style: {colors: "#ccc"},
      formatter: (value) => value.toFixed(2),
    },
  },
  grid: {
    borderColor: "#444"
  },
}